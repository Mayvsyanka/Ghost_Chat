from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta
from typing import Optional

app = FastAPI()

# Змінна для збереження історії запитів (замість бази даних)
query_history_db = []

# Модель для історії запитів
class QueryHistory(BaseModel):
    user_id: int
    query_text: str
    timestamp: datetime

# Модель користувача (приклад, можна використовувати власну модель користувача)
class User(BaseModel):
    username: str
    email: str

# Конфігурація для JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Ініціалізуйте бібліотеки для аутентифікації та хешування паролів
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функція для створення токену
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функція для отримання поточного користувача (приклад)
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Could not validate credentials")
        # Ваша логіка перевірки і аутентифікації користувача
        # Тут потрібно відповідно налаштувати аутентифікацію користувача
        # Приклад: дістати користувача за токеном або іншими методами
        # Поверніть об'єкт користувача, якщо він аутентифікується успішно
    except JWTError:
        raise HTTPException(status_code=400, detail="Could not validate credentials")

# Маршрут для збереження історії запитів
@app.post("/save_query/")
async def save_query(query: QueryHistory, current_user: User = Depends(get_current_user)):
    query_history_db.append(query)
    return {"message": "Query saved successfully"}

# Маршрут для отримання історії запитів
@app.get("/query_history/", response_model=List[QueryHistory])
async def get_query_history(current_user: User = Depends(get_current_user)):
    # Тут ви можете фільтрувати історію запитів за поточним користувачем
    user_query_history = [query for query in query_history_db if query.user_id == current_user.id]
    return user_query_history
