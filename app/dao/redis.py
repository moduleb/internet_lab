from fastapi import HTTPException

from app.logger import logger
from redis_ import r

redis_error_msg = "Redis недоступен"

class RedisDAO:
    @staticmethod
    def add_token(username, token):
        try:
            r.rpush(username, token)
        except Exception as e:
            logger.error(f"{redis_error_msg} {e}")
            raise HTTPException(status_code=500, detail=redis_error_msg)

    @staticmethod
    def check_token(username, token):
        try:
            return token.encode('utf-8') in r.lrange(username, 0, -1)
        except Exception as e:
            logger.error(f"{redis_error_msg} {e}")
            raise HTTPException(status_code=500, detail=redis_error_msg)

    @staticmethod
    def delete_token(username, token):
        try:
            r.lrem(username, 0, token)
        except Exception as e:
            logger.error(f"{redis_error_msg} {e}")
            raise HTTPException(status_code=500, detail=redis_error_msg)
