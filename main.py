#from langchain.agents.agent_types import AgentType
#from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.llms import Ollama
import pandas as pd
from pandasai import SmartDataframe
from cryptography.fernet import Fernet
import time


if __name__ == "__main__":
    df = pd.read_csv('fraudTrain.csv') 
    # Drop columns that are unneccesary
    df.drop(columns=['Unnamed: 0','first', 'last', 'gender', 'street', 'city', 'state', 'zip', 'dob', 'trans_num','trans_date_trans_time'],inplace=True)
    df.dropna() # Drop all rows that have missing values

    llm = Ollama(model="mistral")  
    sdf = SmartDataframe(df, config={"llm": llm})

    submitted_transactions = []
    valid_transactions = []

    with open("dummy_key.txt", "rb") as key_file:
        key = key_file.read()
    f = Fernet(key)

    message = input("Enter prompt: ") 
    while message.lower().strip() not in ['exit', 'end', 'quit', 'stop']: # Stop words
       
        if(message.lower().strip() == 'help'):
            print("exit, end, quit, or stop - terminates the program")
            print('transaction - enters a transaction')
            print('validate - checks to see if any of the transactions are fradulent')
            print("ask - ask the AI a question")
            print("print - prints legitimate transactions")
        elif(message[0:4].lower() == 'ask '):
            start_time = time.time()
            response = sdf.chat(message[4:])
            token = f.encrypt(response.encode())
            print(response)
            print(f.decrypt(token).decode())
            print("Response time: %s seconds" % (time.time() - start_time))
        elif(message[0:7].lower() == 'submit '):
            print(message[7:])
        elif(message[0:11].lower() == 'transaction'):
            print(message[11:])
        else:
            print("Unkwown command. Type 'help' for a list of commands." )

        message = input("Enter prompt: ") 
    print("Terminating program")