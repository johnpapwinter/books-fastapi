from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import UserRequest, LoginRequest
from models.entities import User


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_all_users(self) -> list[UserRequest]:
        result = self.db.query(User).all()
        return [UserRequest.model_validate(user) for user in result]

    def sign_up(self, user: UserRequest) -> UserRequest:
        new_user = User(
            username=user.username,
            email=user.email,
            password=self._get_password_hash(user.password)
        )
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
        except Exception as e:
            print(e)
            self.db.rollback()

        return UserRequest.model_validate(new_user)

    def login(self, login_request: LoginRequest) -> UserRequest:
        user = self.db.query(User).filter(User.username == login_request.username).first()
        if not user:
            raise HTTPException(status_code=401, detail='Incorrect username or password')
        if self._verify_password(login_request.password, user.password):
            return UserRequest.model_validate(user)
        else:
            raise HTTPException(status_code=401, detail='Incorrect username or password')

    def _get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)
