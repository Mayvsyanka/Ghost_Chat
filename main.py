from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



from src.routes import auth, users, access, document, vectorstore, chat

from src.conf.config import Settings


settings = Settings()


app = FastAPI(
    title="PDF-chat API",
    description="API for PDF-chat application",
    version="1.0.0",
)


app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(access.router, prefix='/api')
app.include_router(document.router, prefix='/api')

app.include_router(vectorstore.router, prefix='/api')

app.include_router(chat.router, prefix='/api')


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api", tags=["Root"])
def root():
    return {"message": "Ghost Application"}


@app.get("/", tags=["Root"])
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Welcome to Ghostgram&quot;.
    
    
    :return: A dictionary with a key of message and a value of &quot;welcome to ghostgram&quot;
    :rtype: dict
    """

    return {"message": "Welcome to PDF-chat"}


