from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth import generate_jwt
from database import get_db
from enums import UserRole
from error_messages import ErrorMessages
from models import UserRequest, LoginRequest, LoginResponse, ChangePasswordRequest
from models.entities import User
from service.generic_service import GenericService


class UserService(GenericService[User, UserRequest]):
    def __init__(self, db: Session):
        super().__init__(db, User, UserRequest)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_all_users(self) -> list[UserRequest]:
        user = self.db.query(User).all()
        return [UserRequest.model_validate(user) for user in user]

    def sign_up(self, user: UserRequest) -> UserRequest:
        new_user = UserRequest(
            username=user.username,
            email=user.email,
            password=self._get_password_hash(user.password),
            role=UserRole.USER.value
        )

        return self.create(new_user)

    def login(self, login_request: LoginRequest) -> LoginResponse:
        user = self.db.query(User).filter(User.username == login_request.username).first()
        if not user:
            raise HTTPException(status_code=401, detail=ErrorMessages.INCORRECT_CREDENTIALS.value)
        if self._verify_password(login_request.password, user.password):
            token = generate_jwt(data={"sub": user.username, "role": user.role})
            return LoginResponse(access_token=token, token_type="Bearer", username=user.username)
        else:
            raise HTTPException(status_code=401, detail=ErrorMessages.INCORRECT_CREDENTIALS.value)

    def change_password(self, change_password_request: ChangePasswordRequest) -> UserRequest:
        user = self.db.query(User).filter(User.id == change_password_request.id).first()
        if not user:
            raise HTTPException(status_code=401, detail=ErrorMessages.INCORRECT_CREDENTIALS.value)
        if self._verify_password(change_password_request.old_password, user.password):
            update_user = UserRequest(
                id=user.id,
                username=user.username,
                email=user.email,
                password=self._get_password_hash(change_password_request.new_password),
                role=user.role
            )
            return self.update(user, update_user.model_dump(exclude_unset=True))
        else:
            raise HTTPException(status_code=401, detail=ErrorMessages.INCORRECT_CREDENTIALS.value)

    def _get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)


def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)
