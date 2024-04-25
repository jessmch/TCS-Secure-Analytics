#from typing import Any, Dict, Iterator, List, Mapping, Optional

# LangChain 
# pip install langchain
#from langchain_core.callbacks.manager import CallbackManagerForLLMRun
#from langchain_core.language_models.llms import LLM
#from langchain_core.outputs import GenerationChunk

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain.document_loaders.csv_loader import CSVLoader

# Imports for embedding
# Embedding turns text into a vector representation
# Useful for comparing texts in vector space (looking at scores instead of text itself)
#
# pip install langchain_openai
from langchain_openai import OpenAIEmbeddings

# Imports for Vectorstores
# Needed to store and search through unstructured data
# Our vector embeds will be stored here
#
# pip install faiss-cpu
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains.combine_documents import create_stuff_documents_chain

#llm = ChatOpenAI(api_key='sk-proj-tfIWz45wld3XFSBc38wyT3BlbkFJczgkVDphbf3KnwYwl6fk')

loader = CSVLoader(file_path='C:/Users/huule/Desktop/School/cs180/archive/fraudTrain.csv')
data = loader.load()

embeddings = OpenAIEmbeddings(api_key='sk-proj-tfIWz45wld3XFSBc38wyT3BlbkFJczgkVDphbf3KnwYwl6fk')

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(data)
vector = FAISS.from_documents(documents, embeddings)

results = vector.similarity_search('Do you have a free plan?')
print(results)

# prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

# <context>
# {context}
# </context>

# Question: {input}""")

# document_chain = create_stuff_documents_chain(llm, prompt)