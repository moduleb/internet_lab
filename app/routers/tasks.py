from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.container import task_service
from app.database import get_session
from app.dto.task import ShowTask, TaskDTO, ShowTasks
from app.services.authentication import AuthenticationService

router = APIRouter()


# """CREATE TASK"""
@router.post("/", response_model=ShowTask,
             summary="Create Task",
             description=" - Возвращает JSON с информацией о созданной записи 'task'\n"
                         " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
async def create(data: TaskDTO = None, current_username: str = Depends(AuthenticationService.verify_token),
                 session: Session = Depends(get_session)):
    return task_service.create(data, session)


# """GET ALL TASKS"""
@router.get("/", response_model=List[ShowTask],
            summary="Get all tasks'",
            description=" - Возвращает JSON с информацией обо всех записях 'task'\n"
                        " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
async def get_all(current_username: str = Depends(AuthenticationService.verify_token),
                  session: Session = Depends(get_session)):
    all_tasks = task_service.get_all(session)
    return jsonable_encoder(all_tasks)


# """GET TASK BY ID"""
@router.get("/{task_id}", response_model=ShowTask,
            summary="Get task by ID'",
            description=" - Возвращает JSON с информацией о найденной по id записи 'task'\n"
                        " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
async def get_one(task_id: int, current_username: str = Depends(AuthenticationService.verify_token),
                  session: Session = Depends(get_session)):
    return task_service.get_one(task_id, session)


# """UPDATE TASK"""
@router.put("/{task_id}", response_model=ShowTask,
            summary="Update task'",
            description=" - Возвращает JSON с информацией о найденной по id записи 'task'\n"
                        " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
async def get_one(task_id: int, data: TaskDTO = None,
                  current_username: str = Depends(AuthenticationService.verify_token),
                  session: Session = Depends(get_session)):
    return task_service.update(task_id, data, session)


# """DELETE TASK"""
@router.delete("/{task_id}",
               summary="Delete task'",
               description=" - Возвращает JSON с информацией о найденной по id записи 'task'\n"
                           " - Требует наличия токена в заголовке запроса в поле 'Authorization'")
async def get_one(task_id: int, current_username: str = Depends(AuthenticationService.verify_token),
                  session: Session = Depends(get_session)):
    task_service.delete(task_id, session)

    return 204
