from typing import Any

from fastapi import APIRouter, Depends
from starlette import status

from auth import filter_for_role
from enums import UserRole
from models import LoginRequest, UserRequest, ChangePasswordRequest, LoginResponse
from service.user_service import UserService, get_user_service

user_router = APIRouter(prefix="/auth")


@user_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(login_request: LoginRequest, service: UserService = Depends(get_user_service)):
    return service.login(login_request)


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRequest)
async def register(user_request: UserRequest, service: UserService = Depends(get_user_service)):
    return service.sign_up(user_request)


@user_router.get("/get-all", status_code=status.HTTP_200_OK, response_model=list[UserRequest])
async def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()


@user_router.patch("/change-password", status_code=status.HTTP_200_OK, response_model=UserRequest)
async def change_password(change_password_request: ChangePasswordRequest,
                          service: UserService = Depends(get_user_service),
                          payload: Any = Depends(filter_for_role(UserRole.ANY))):

    return service.change_password(change_password_request)


@user_router.get("/admin")
async def get_admin(payload: Any = Depends(filter_for_role(UserRole.ADMIN))):
    return {"message": f"You are an admin"}


@user_router.get("/user")
async def get_user(payload: Any = Depends(filter_for_role(UserRole.USER))):
    return {"message": f"You are an user"}
