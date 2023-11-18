from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = input("OpenAI API Key: ")

async def doc_to_vectorstore(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    text_splitter = CharacterTextSplitter(separator="\n\n",
                                          chunk_size=1000,
                                          chunk_overlap=200)

    chunks = text_splitter.split_documents(documents=pages)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)
    vectorstore = db.serialize_to_bytes()

    output_folder = 'src/store'
    print(f"{os.path.basename(file_path)[:-4]}.pkl")
    output_file = os.path.join(output_folder, f"{os.path.basename(file_path)[:-4]}.pkl")
    with open(output_file, "wb") as f:
        f.write(vectorstore)

    return vectorstore