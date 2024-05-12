from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_community.llms import Ollama
import pandas as pd
from pandasai import SmartDataframe


if __name__ == "__main__":
    df = pd.read_csv('archive\\fraudTrain.csv') 
    llm = Ollama(model="mistral")  
    sdf = SmartDataframe(df, config={"llm": llm})


    message = input("Enter prompt: ") 
    while message.lower().strip() != 'exit': # Typing "end" will close our connection and end our program
       
        print(sdf.chat(message))

        message = input("Enter prompt: ") 