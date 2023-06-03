import uvicorn
from fastapi import FastAPI

from app.limiter import limiter
from app.routers import tasks, login, register

# Создаем приложение
app = FastAPI()

app.state.limiter = limiter

# Регистрируем эндпоинты
app.include_router(register.router, prefix='/register', tags=["/register"])
app.include_router(login.router, prefix='/login', tags=["/login"])
app.include_router(tasks.router, prefix='/tasks', tags=["/tasks"])

# Запускаем приложение
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
