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

def doc_to_vectorstore(file_path):

    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 100)
    chunks = text_splitter.split_documents(documents=pages)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    with open(f"{file_path[:-4]}.pkl", "wb") as f:
        pickle.dump(vectorstore, f)

    return vectorstore

