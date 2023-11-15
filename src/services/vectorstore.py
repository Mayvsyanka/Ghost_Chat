import pickle

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = input("OpenAI API Key: ")

async def doc_to_vectorstore(file_content, file_path):

    text_splitter = CharacterTextSplitter(separator="\n\n", 
                                          chunk_size = 1000, 
                                          chunk_overlap = 200)
    
    chunks = text_splitter.split_documents(documents=file_content)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    with open(f"{file_path[:-4]}.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

    return vectorstore

