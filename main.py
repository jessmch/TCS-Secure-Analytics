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

    start_time = time.time()
    keep_columns = ['category','amt','zip','lat','long','city_pop','merch_lat','merch_long','is_fraud']
    
    # Load the training data
    print('Loading training set')
    df = pd.read_csv('fraudTrain.csv')
    df.dropna() # Drop all rows that have missing values
    print('Training set loaded')

    # Load the LLM
    print('Loading Ollama model')
    llm = Ollama(model="mistral")  
    sdf = SmartDataframe(df, config={"llm": llm})
    print('Ollama loaded')

    with open("dummy_key.txt", "rb") as key_file:
        key = key_file.read()
    f = Fernet(key)

    # Load the MLM
    print('Generating Prediction Model')
    train = df[keep_columns]
    # Convert categories to dummy variables
    train = pd.get_dummies(train, drop_first=True)
    y_train = train['is_fraud'].values
    X_train = train.drop("is_fraud", axis='columns').values

    model = RandomForestClassifier(random_state=5)
    model.fit(X_train, y_train)
    print('Prediction Model created')

    # Pre-process test data
    # Should be in the same format as the original CSV
    print(f'Predicting data in fraudTest.csv')
    test = pd.read_csv('fraudTest.csv')
    test_data = test[keep_columns]
    test_data = pd.get_dummies(test_data, drop_first=True)
    y_test = test_data['is_fraud'].values
    X_test = test_data.drop("is_fraud", axis='columns').values

    predictions = model.predict(X_test)

    # Generate the accuracy report
    print(f'Classification report:{classification_report(y_test, predictions)}')
    conf_mat = confusion_matrix(y_true=y_test, y_pred=predictions)
    print(f'Confusion matrix:{conf_mat}')

    # Generate an output to a csv file
    #output = pd.DataFrame({'first': test_data.first,
    #                       'last': test_data.last,
    #                       'is_fraud': predictions})
    #output.to_csv('output.csv', index=False)
    #print('Output saved to output.csv')

    # Ask the LLM some questions
    print('Query:', 'How many rows are there?')
    response = sdf.chat('How many rows are there?')
    print('Response:', response)
    print()

    print('Query:', 'What is the biggest spending category?')
    response = sdf.chat('What is the biggest spending category?')
    print('Response:', response)
    print()

    print('Query:', 'What is the average spending amount?')
    response = sdf.chat('What is the average spending amount?')
    print('Response:', response)
    print()

    print(f"\nResponse time: {(time.time() - start_time)} seconds")

    # simulate long-running process for memory dump
    time.sleep(300)

    print('Finishing program')