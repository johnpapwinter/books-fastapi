from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from enums import UserRole
from models import User

JWT_SECRET = "my_secret"
JWT_ALGORITHM = "HS256"
JWT_DEFAULT_EXPIRATION_HOURS = 8


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
                     db: Session = Depends(get_db)):
    token = credentials.credentials
    username = decode_jwt(token)

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def filter_for_role(required_role: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        if required_role.name == UserRole.ANY:
            return current_user
        if current_user.role != required_role.name:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Insufficient rights")
        return current_user

    return role_checker


def generate_jwt(data: dict, expires_in: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_in:
        expire = datetime.now() + expires_in
    else:
        expire = datetime.now() + timedelta(hours=JWT_DEFAULT_EXPIRATION_HOURS)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return encoded_jwt


def decode_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')

    return username

