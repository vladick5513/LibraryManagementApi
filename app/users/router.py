from fastapi import APIRouter, HTTPException
from starlette import status

from app.users.auth import get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister

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