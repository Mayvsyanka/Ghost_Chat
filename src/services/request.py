from langchain import OpenAI
from langchain.chains.question_answering import load_qa_chain

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

import os
from dotenv import load_dotenv

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = input("OpenAI API Key: ")

def load_vectorstore(file_path):
    
    with open(file_path, "rb") as f:
        vectorstore_bytes = f.read()

    embeddings = OpenAIEmbeddings()  
    vectorstore = FAISS.deserialize_from_bytes(vectorstore_bytes, embeddings)

    return vectorstore

def request_answer_from_llm(vectorstore, question):
    
    if question:
        doc = vectorstore.similarity_search(query=question, k=3)

        llm = OpenAI(temperature=0.7)
        chain = load_qa_chain(llm=llm, chain_type="stuff")

        response = chain.run(input_documents=doc, question=question)
        return response

    return response



