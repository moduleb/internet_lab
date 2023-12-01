import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database import db
from app.logger import log
from app.routers import users, login, register, logout

# создание приложения
app = FastAPI()

# перенаправление на /docs при обращении на "/"
@app.get("/", response_class= RedirectResponse)
def redirect():
    return "/docs"

# регистрация эндпоинтов
app.include_router(users.router, prefix='/users', tags=["/users"])
app.include_router(login.router, prefix='/users', tags=["/login"])
app.include_router(logout.router, prefix='/users', tags=["/logout"])
app.include_router(register.router, prefix='/users', tags=["/register"])

# log.debug(db.is_connected())

# запуск приложения
if __name__ == "__main__":
     log.info(f'Загружена конфигурация {os.environ.get("FASTAPI_ENV")}')
     uvicorn.run(app, host="0.0.0.0")

