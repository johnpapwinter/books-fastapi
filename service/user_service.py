from datetime import timedelta, datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import UserRequest, LoginRequest, LoginResponse
from models.entities import User
from service.generic_service import GenericService


class UserService(GenericService[User, UserRequest]):
    def __init__(self, db: Session):
        super().__init__(db, User, UserRequest)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = "my_secret"
        self.default_expiration_hours = 8

    def get_all_users(self) -> list[UserRequest]:
        user = self.db.query(User).all()
        return [UserRequest.model_validate(user) for user in user]

    def sign_up(self, user: UserRequest) -> UserRequest:
        new_user = UserRequest(
            username=user.username,
            email=user.email,
            password=self._get_password_hash(user.password),
            role="USER"
        )

        return self.create(new_user)

    def login(self, login_request: LoginRequest) -> LoginResponse:
        user = self.db.query(User).filter(User.username == login_request.username).first()
        if not user:
            raise HTTPException(status_code=401, detail='Incorrect username or password')
        if self._verify_password(login_request.password, user.password):
            token = self._generate_jwt(data={"sub": user.username, "role": user.role})
            return LoginResponse(access_token=token, token_type="Bearer", username=user.username)
        else:
            raise HTTPException(status_code=401, detail='Incorrect username or password')

    def verify_token(self, credentials: HTTPAuthorizationCredentials) -> UserRequest:
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail='Invalid authentication credentials')
            user = self.db.query(User).filter(User.username == username).first()
            if user is None:
                raise HTTPException(status_code=401, detail='User not found')

            return UserRequest.model_validate(user)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def _get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def _generate_jwt(self, data: dict, expires_in: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_in:
            expire = datetime.now() + expires_in
        else:
            expire = datetime.now() + timedelta(hours=self.default_expiration_hours)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm='HS256')
        return encoded_jwt


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)
