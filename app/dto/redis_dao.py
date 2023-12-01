from typing import List

from fastapi import HTTPException

from app.logger import log
from app.redis_ import r

REDIS_ERROR_MSG = "Redis error"


class RedisDAO:
    """
    Класс для работы с хранилищем Redis
    """
    @staticmethod
    def add_token(username: str, token: str) -> None:
        """
        Добавление токена в список деактивированных токенов пользователя
        """
        try:
            result = r.rpush(username, token)
            log.debug(f"Добавление токена в список деактивированных: {result}")
        except Exception as e:
            log.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)

    @staticmethod
    def check_token(username: str, token: str) -> bool:
        """
        Проверка наличия токена в списке деактивированных токенов пользователя
        """
        try:
            # получаем список всех токенов, хранящихся с ключем username
            # 0 - индекс начала поиска (с самого начала)
            # -1 - индекс конца поиска (до самого конца)
            tokens: List[bytes] = r.lrange(username, 0, -1)

            # Redis сохраняет токены в байтах, поэтому преобразуем в байты входящий токен
            result = token.encode("utf-8") in tokens

            log.debug(f"Проверка наличия токена в списке деактивированных: {result}")
            return result
        except Exception as e:
            log.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)