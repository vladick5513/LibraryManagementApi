from fastapi import APIRouter, HTTPException, Response, Depends
from starlette import status

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import SUserRegister, SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register/")
async def register_user(user_data: SUserRegister):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    await UsersDAO.create(**user_dict)
    return {"message": f'Вы успешно зарегистрированы!'}

@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Неверная почта или пароль")
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="user_access_token", value=access_token,  httponly=True)
    return {"access_token": access_token, "refresh_token": None}

@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}