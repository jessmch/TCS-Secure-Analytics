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


if __name__ == "__main__":

    keep_columns = ['category','amt','zip','lat','long','city_pop','merch_lat','merch_long','is_fraud']
    df = pd.read_csv('fraudTrain.csv')
    # Drop columns that are unneccesary
    #df.drop(columns=['lat', 'long', 'city_pop', 'job', 'unix_time', 'merch_lat', 'merch_long', 'Unnamed: 0','first', 'last', 'gender', 'street', 'state', 'zip', 'dob', 'trans_num','trans_date_trans_time'],inplace=True)
    df.dropna() # Drop all rows that have missing values

    llm = Ollama(model="mistral")  
    sdf = SmartDataframe(df, config={"llm": llm})

    submitted_transactions = []
    valid_transactions = []

    model = None

    with open("dummy_key.txt", "rb") as key_file:
        key = key_file.read()
    f = Fernet(key)

    print('Welcome to the TCS Black Box Test!')
    message = input("Enter a prompt: ") 
    while message.lower().strip() not in ['exit', 'end', 'quit', 'stop']: # Stop words
       
        start_time = time.time()
        if(message.lower().strip() == 'help'):
            print("exit, end, quit, or stop - terminates the program")
            print('enter transaction        - enters a transaction')
            print("transactions             - list entered transactions")
            print('validate transactions    - checks to see if any of the transactions are fradulent')
            print("ask                      - ask the AI a question")
            print("generate model           - generates a prediction model for the data")
            print("generate output          - shows the predicted frauds and the accuracy report")
            print("print                    - prints legitimate transactions")
            print("echo                     - echoes the last message")
        elif(message[0:4].lower() == 'ask '):
            #response = message[4:]
            response = sdf.chat(message[4:])

            # Encrypt our responses
            token = f.encrypt(str(response).encode())

            # Save our responses to a file
            #f = open('responses.txt', 'a')
            #f.write()
            #f.close()

            print("response:", f.decrypt(token).decode())
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
                print(f"""Credit Card: {transaction['cc_num']}
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

            print("Prediction Model created")
        elif(message.lower().strip() == 'generate output'):
            test_csv = input('Name of the CSV file to predict from: ')

            # Pre-process test data
            # Should be in the same format as the original CSV
            test = pd.read_csv(test_csv)
            test_data = test[keep_columns]
            test_data = pd.get_dummies(test_data, drop_first=True)
            y_test = test_data['is_fraud'].values
            X_test = test_data.drop("is_fraud", axis='columns').values

            print(test_data.columns)

            predictions = model.predict(X_test)

            print('Classification report:\n', classification_report(y_test, predictions))
            conf_mat = confusion_matrix(y_true=y_test, y_pred=predictions)
            print('Confusion matrix:\n', conf_mat)

            #output = pd.DataFrame({'first': test_data.first,
            #                       'last': test_data.last,
            #                       'is_fraud': predictions})
            #output.to_csv('output.csv', index=False)
            #print('Output saved to output.csv')

        elif(message[0:4].lower() == 'echo'):
            response = message[4:]

            # Encrypt our responses
            token = f.encrypt(str(response).encode())
            print('response:', response, token)
        else:
            print("Unkwown command. Type 'help' for a list of commands." )
        print("Response time: %s seconds" % (time.time() - start_time))

        message = input("Enter prompt: ") 
    print("Terminating program")