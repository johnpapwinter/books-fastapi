from fastapi import APIRouter, Depends
from starlette import status

from models import LoginRequest, UserRequest
from service.user_service import UserService, get_user_service

user_router = APIRouter(prefix="/auth")


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_request: LoginRequest, service: UserService = Depends(get_user_service)):

    return service.login(login_request)


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRequest)
async def register(user_request: UserRequest, service: UserService = Depends(get_user_service)):

    return service.sign_up(user_request)


@user_router.get("/get-all", status_code=status.HTTP_200_OK, response_model=list[UserRequest])
async def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

