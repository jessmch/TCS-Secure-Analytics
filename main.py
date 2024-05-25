#from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.llms import Ollama
from pandasai import SmartDataframe
from cryptography.fernet import Fernet
import pandas as pd
import time

import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score 

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import socket
import sys

PORT = 3389
HOST = "0.0.0.0"

if __name__ == "__main__":

    keep_columns = ['category','amt','zip','lat','long','city_pop','merch_lat','merch_long','is_fraud']

    print('Loading training set')
    df = pd.read_csv('fraudTrain.csv')
    # Drop columns that are unneccesary
    #df.drop(columns=['lat', 'long', 'city_pop', 'job', 'unix_time', 'merch_lat', 'merch_long', 'Unnamed: 0','first', 'last', 'gender', 'street', 'state', 'zip', 'dob', 'trans_num','trans_date_trans_time'],inplace=True)
    df.dropna() # Drop all rows that have missing values
    print('Training set loaded')


    print('Loading Ollama model')
    llm = Ollama(model="mistral")  
    sdf = SmartDataframe(df, config={"llm": llm})
    print('Ollama loaded')

    submitted_transactions = []
    valid_transactions = []
    model = None

    with open("dummy_key.txt", "rb") as key_file:
        key = key_file.read()
    f = Fernet(key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((HOST, PORT))
        srv.listen()

        print("Server listening on port", PORT)

        while True:
            connection, address = srv.accept()

            with connection:
                print(f"Client connected from {address}")

                while True:
                    output = 'Server Response:\n'
                    message = connection.recv(4096).decode()
                    print("Received message:", message)

                    start_time = time.time()
                    if(message.lower().strip() == 'help'):
                        output += '''
                        exit, end, quit, or stop   - terminates the program
                        enter transaction          - enters a transaction
                        transactions               - list entered transactions
                        validate transactions      - checks to see if any of the transactions are fradulent
                        ask <query>                - ask the AI a question
                        generate model             - generates a prediction model for the data
                        generate output <csv file> - shows the predicted frauds and the accuracy report
                        print                      - prints legitimate transactions
                        echo <message>             - echoes the last message
                        '''
                    elif(message[0:4].lower() == 'ask '):
                        response = sdf.chat(message[4:])

                        # Encrypt our responses
                        token = f.encrypt(str(response).encode())

                        output += f.decrypt(token).decode()
                    elif(message.lower().strip() == 'enter transaction'):
                        transaction_info = dict.fromkeys(df.columns)
                        info = input('Enter credit card number: ')
                        transaction_info['cc_num'] = info
                        info = input('Enter name: ')
                        transaction_info['merchant'] = info
                        info = input('Enter reason of purchase: ')
                        transaction_info['category'] = info
                        info = input('Enter the amount: ')
                        transaction_info['amt'] = info
                        info = input('Enter the city: ')
                        transaction_info['city'] = info
                        submitted_transactions.append(transaction_info)
                        print(message[7:])
                    elif(message.lower().strip() == 'transactions'):
                        for transaction in submitted_transactions:
                            print(f"""
                                Credit Card: {transaction['cc_num']}
                                Merchant Name: {transaction['merchant']}
                                Category: {transaction['category']}
                                Transaction Amount: {transaction['amt']}
                                City of Transaction: {transaction['city']}""")
                            print()
                    elif(message.lower().strip() == 'validate transactions'):
                        response = sdf.chat(f"Is {submitted_transactions[0]} a valid transaction?")
                        print(response)
                    elif(message.lower().strip() == 'generate model'):
                        train = df[keep_columns]
                        # Convert categories to dummy variables
                        train = pd.get_dummies(train, drop_first=True)
                        y_train = train['is_fraud'].values
                        X_train = train.drop("is_fraud", axis='columns').values

                        model = RandomForestClassifier(random_state=5)
                        model.fit(X_train, y_train)

                        output += "Prediction Model created"
                    elif(message[0:15].lower().strip() == 'generate output'):
                        test_csv = response = message[15:]

                        # Pre-process test data
                        # Should be in the same format as the original CSV
                        test = pd.read_csv(test_csv)
                        test_data = test[keep_columns]
                        test_data = pd.get_dummies(test_data, drop_first=True)
                        y_test = test_data['is_fraud'].values
                        X_test = test_data.drop("is_fraud", axis='columns').values

                        predictions = model.predict(X_test)

                        output += f'Classification report:{classification_report(y_test, predictions)}\n'
                        conf_mat = confusion_matrix(y_true=y_test, y_pred=predictions)
                        output += f'Confusion matrix:{conf_mat}\n'

                        #output = pd.DataFrame({'first': test_data.first,
                        #                       'last': test_data.last,
                        #                       'is_fraud': predictions})
                        #output.to_csv('output.csv', index=False)
                        #print('Output saved to output.csv')

                    elif(message[0:4].lower() == 'echo'):
                        response = message[4:]

                        # Encrypt our responses
                        token = f.encrypt(str(response).encode())
                        output += f'{response} {token}'
                    else:
                        output += "Unkwown command. Type 'help' for a list of commands."
                    output += f"\nResponse time: {(time.time() - start_time)} seconds"

                    if not message:
                        break
                    print(output)
                    connection.sendall(output.encode())

                print("Client disconnected")      
        