from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.container import user_service, auth_service
from app.database import get_session
from app.dto.user import UserLoginDTO


router = APIRouter()


@router.post("/", summary="Авторизация пользователя",
             description=" - Принимает username и password существующего пользователя, \n - Возвращает токен доступа на 30 минут")

async def login(data: UserLoginDTO, session: Session = Depends(get_session)):
    # form_data: OAuth2PasswordRequestForm = Depends()

    # Получаем объект пользователя из базы данных
    user = user_service.get_user(data.username, session)

    if not user:
        raise HTTPException(404, detail="Пользователь не найден")

    # Хешируем полученный из запроса пароль
    password2 = user_service.hash_password(data.password)

    # Сравниваем пароль из базы данных с хешированным паролем из запроса
    # Если все ОК, генерируем и возвращаем токен
    if user.password == password2:
        access_token = auth_service.create_access_token(user.username)

        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(401, detail="Неверный логин или пароль")
