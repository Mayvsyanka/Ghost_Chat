#v2
from langchain import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import CallbackManager, get_openai_callback
from langchain.documents import Document

def request_answer_from_llm(vectorstore, question):

    callback_manager = CallbackManager([get_openai_callback()])
    llm = OpenAI(temperature=0.7, 
                 callbacks=callback_manager) #Ініціалізується модель мови OpenAI, temperature - креативність відповіді 

    chain = load_qa_chain(llm=llm, 
                          chain_type="stuff")# завантажується ланцюг відповідей на питання

    docs = [Document(page_content=doc) for doc in vectorstore.similarity_search(query=question, k=3)]#Виконується пошук подібності за допомогою vectorstore та введеного question


    response = chain.run(input_documents=docs, 
                         question=question)#Запускається ланцюг відповідей

    return response
