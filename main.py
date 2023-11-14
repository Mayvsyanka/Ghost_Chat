from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.routes import auth, users, access, document, vectorstore

from src.conf.config import settings

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(access.router, prefix='/api')
app.include_router(document.router, prefix='/api')
app.include_router(vectorstore.router, prefix='/api')


@app.get("/", tags=["Root"])
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Welcome to Ghostgram&quot;.
    
    
    :return: A dictionary with a key of message and a value of &quot;welcome to ghostgram&quot;
    :rtype: dict
    """
    return {"message": "Welcome to Ghostgram"}


