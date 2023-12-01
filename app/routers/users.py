from sqlite3 import Cursor

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.database import get_cursor
from app.dto.user_dto import UserDTO
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


# GET ONE
@router.get("/", summary="Получение информации о пользователе",
            description=" - Возвращает username, email пользователя \n"
                        " - Требует get параметра с id пользователя")
async def get_one(cursor=Depends(get_cursor),
                  username=Depends(AuthService.verify_token)) -> Response:
    data = UserService.get_one_by_username(cursor, username)
    json_data = jsonable_encoder({'data': data})
    return JSONResponse(content=json_data)


# GET ALL
# @router.get("/", summary="Get User Info",
#             description=" - Возвращает username, email пользователя \n"
#                         " - Требует get параметра с id пользователя")
# async def get_all(cursor=Depends(get_cursor)) -> Response:
#     data = UserService.get_all(cursor)
#     json_data = jsonable_encoder({'data': data})
#     return JSONResponse(content=json_data)


@router.put("/{user_id}",
            summary="Update User",
            description=" - Возвращает username, email пользователя \n"
                        " - Требует get параметра с id пользователя")
async def update(data: UserDTO,
                 cursor: Cursor = Depends(get_cursor),
                 username=Depends(AuthService.verify_token)) -> Response:
    data.password = AuthService.hash_pass(data.password)
    UserService.update(cursor, username, data)
    data = UserService.get_one_by_username(cursor, username)
    json_data = jsonable_encoder({'data': data})
    return JSONResponse(content=json_data)


@router.delete("/", status_code=204,
               summary="Delete User",
               description=" - Возвращает username, email пользователя \n"
                           " - Требует get параметра с id пользователя")
async def delete(cursor=Depends(get_cursor),
                 username=Depends(AuthService.verify_token)):
    UserService.delete(cursor, username)
