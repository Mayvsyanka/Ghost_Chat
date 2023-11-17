"""Module for authorization and authentication operations"""

from fastapi.responses import HTMLResponse
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request, Form, Path
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email, send_email_forgot
import hashlib
from fastapi.templating import Jinja2Templates
import os
from fastapi.responses import RedirectResponse

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()
templates = Jinja2Templates(directory="templates")


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):

    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):

    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created"}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    if user.access is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You was banned")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):

    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/reset-password/request', response_model=dict)
async def request_password_reset(body: RequestEmail, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print("start")
    user = await repository_users.get_user_by_email(body.email, db)
    if user:

        base_url = "http://127.0.0.1:8000/api/auth"  # Замени на свой base_url
        link = f"{base_url}/reset-password/reset/{user.email}"

        background_tasks.add_task(send_email_forgot, user.email, link)

    return {"message": f"If an account with this email exists, you'll receive an email with instructions to reset your password."}

templates = Jinja2Templates(
    directory="C:\\Projects\\Homeworks Data Sciense\\final_ds\\src\\routes\\templates")

@router.get('/reset-password/reset/{email}', response_class=HTMLResponse)
async def show_reset_password_form(email: str, request: Request):
    return templates.TemplateResponse("reset_password_template.html", {"request": request, "email": email})


@router.post('/reset-password/reset/{email}', response_model=dict)
async def reset_password(email: str, new_password: str = Form(...), db: Session = Depends(get_db)):

    user = await repository_users.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")

    hashed_password = auth_service.get_password_hash(new_password)
    await repository_users.update_password(user.id, hashed_password, db)

    redirect_url = "http://127.0.0.1:3000"  # Замените на свой URL
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
