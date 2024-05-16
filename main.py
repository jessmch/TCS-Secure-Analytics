#from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.llms import Ollama
import pandas as pd
from pandasai import SmartDataframe
from cryptography.fernet import Fernet
import time


if __name__ == "__main__":
    df = pd.read_csv('fraudTrain.csv') 
    # Drop columns that are unneccesary
    df.drop(columns=['lat', 'long', 'city_pop', 'job', 'unix_time', 'merch_lat', 'merch_long', 'Unnamed: 0','first', 'last', 'gender', 'street', 'state', 'zip', 'dob', 'trans_num','trans_date_trans_time'],inplace=True)
    df.dropna() # Drop all rows that have missing values

    llm = Ollama(model="mistral")  
    sdf = SmartDataframe(df, config={"llm": llm})

    submitted_transactions = []
    valid_transactions = []

    with open("dummy_key.txt", "rb") as key_file:
        key = key_file.read()
    f = Fernet(key)

    print('Welcome to the TCS Black Box Test!')
    message = input("Enter a prompt: ") 
    while message.lower().strip() not in ['exit', 'end', 'quit', 'stop']: # Stop words
       
        start_time = time.time()
        if(message.lower().strip() == 'help'):
            print("exit, end, quit, or stop - terminates the program")
            print('transaction - enters a transaction')
            print('validate - checks to see if any of the transactions are fradulent')
            print("ask - ask the AI a question")
            print("print - prints legitimate transactions")
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
        elif(message.lower().strip() == 'test'):
            print(df.head(1))
            print(sdf.chat(f"is {df.head(1)} a valid transaction?"))
        else:
            print("Unkwown command. Type 'help' for a list of commands." )
        print("Response time: %s seconds" % (time.time() - start_time))

        message = input("Enter prompt: ") 
    print("Terminating program")