from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import get_cursor
from app.dto.user_dto import UserRegDTO
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


# REGISTER
@router.post("/register",
             summary="Create User",
             description=" - Возвращает username, email пользователя \n"
                         " - Требует get параметра с id пользователя")
async def create(request: UserRegDTO, cursor = Depends(get_cursor)) -> Response:

    request.password = AuthService.hash_pass(request.password)
    user_id = await UserService.create(cursor, request)
    user_data = await UserService.get_one(cursor, user_id)

    access_token = AuthService.create_access_token(user_data['username'])
    data = {'data': user_data, "access_token": access_token, "token_type": "bearer"}
    json_data = jsonable_encoder(data)
    return JSONResponse(content=json_data)
