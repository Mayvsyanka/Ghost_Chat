from langchain.embeddings import OpenAIEmbeddings 
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
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
    db = FAISS.from_documents(chunks, embeddings)
    vectorstore = db.serialize_to_bytes() 

    output_folder = 'src/store'
    with open(os.path.join(output_folder, f"{os.path.basename(file_path)[:-4]}.pkl"), "wb") as f:
        f.write(vectorstore)
        print("Done!")
    
    return vectorstore

