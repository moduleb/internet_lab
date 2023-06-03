from typing import Type

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.logger import logger
from app.models.task import Task


class TaskDAO:
    def create(self, new_task: Task, session: Session) -> Task:
        """
        Добавляет новый task в базу данных.
        """
        try:
            # Создание нового task и сохранение изменений в базе данных
            session.add(new_task)
            session.commit()

        except IntegrityError as e:
            # Если уже существует
            if 'already exists' in str(e):
                raise HTTPException(500, detail="Task уже существует")

        except Exception as e:
            # Если произошла какая-либо другая ошибка
            logger.error(f"[TaskDAO] Ошибка базы данных: {e}")
            raise HTTPException(500, detail="Ошибка базы данных")

        else:
            # Если ошибок не возникло, возвращаем созданный task
            return new_task

    def get_one(self, task_id: int, session: Session) -> Task:
        """
        Извлекает task с заданным id из базы данных.
        """
        try:
            return session.query(Task).filter(Task.id == task_id).first()

        except Exception as e:
            logger.error(f"[TaskDAO] Ошибка базы данных: {e}")
            raise HTTPException(500, detail="Ошибка базы данных")

    def get_all(self, session: Session) -> list[Type[Task]]:
        """
        Извлекает все объекты task из базы данных.
        """
        try:
            return session.query(Task).all()

        except Exception as e:
            logger.error(f"[TaskDAO] Ошибка базы данных: {e}")
            raise HTTPException(500, detail="Ошибка базы данных")

    def update(self, task: Task, session: Session) -> Task:
        """
        Добавляет новый task в базу данных.
        """
        try:
            # Обновление task и сохранение изменений в базе данных
            session.add(task)
            session.commit()

        except Exception as e:
            logger.error(f"[TaskDAO] Ошибка базы данных: {e}")
            raise HTTPException(500, detail="Ошибка базы данных")

        else:
            # Если ошибок не возникло, возвращаем обновленный task
            return task

    def delete(self, task: Task, session: Session):
        """
        Удаляет task из базы данных.
        """
        try:
            session.delete(task)
            session.commit()

        except Exception as e:
            logger.error(f"[TaskDAO] Ошибка базы данных: {e}")
            raise HTTPException(500, detail="Ошибка базы данных")
