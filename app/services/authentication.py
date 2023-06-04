from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.config import config
from app.dao.redis import RedisDAO
from app.logger import logger


class AuthenticationService:
    def __init__(self, redis_dao: RedisDAO):
        self.redis = redis_dao

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def create_access_token(self, username: str) -> bytes:
        """
        Генерирует токен доступа
        :param username:
        :return: token
        """
        data = {"username": username}

        # Устанавливаем время жизни токена и записываем в data
        expire = datetime.utcnow() + timedelta(minutes=config.token.EXPIRATION_TIME_MINUTES)
        data_to_encode = {**data, **{"exp": expire}}

        # Генерируем токен
        token = jwt.encode(data_to_encode, config.token.SECRET, algorithm=config.token.ALGORITHM)

        # Возвращаем токен
        return token

    def verify_token(self, token: str = Depends(oauth2_scheme)) -> str:
        """
        Декодирует токен и проверяет его наличие
        в списке неактивных токенов пользователя в Redis
        :param token:
        :return: username
        """
        data = self._decode_token(token)
        username = data.get("username")

        if username is None:
            raise HTTPException(status_code=401, detail="Неверные данные для аутентификации")

        # Проверяем наличие токена в списке неактивных токенов пользователя в Redis
        if self.redis.check_token(username, token):
            raise HTTPException(status_code=401, detail="Токен недействителен")

        return username

    def logout(self, token: str = Depends(oauth2_scheme)) -> str:
        """
        Декодирует токен и добавляет его в список неактивных токенов пользователя в Redis
        :param token:
        :return: username
        """
        data = self._decode_token(token)

        username = data.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Неверные данные для аутентификации")

        # Сохраняем в список неактивных токенов пользователя в Redis
        self.redis.add_token(username, token)

        # Возвращаем username
        return username

    @staticmethod
    def _decode_token(token: str) -> dict:
        """
        Декодирует токен (извлекает data)
        :param token:
        :return: data
        """
        try:
            data = jwt.decode(token, config.token.SECRET, algorithms=[config.token.ALGORITHM])

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок действия токена истек")

        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="Недействительная подпись токена")

        except jwt.DecodeError:
            logger.error(f'Ошибка декодирования токена: {e}')
            raise HTTPException(status_code=401, detail="Ошибка декодирования токена")

        return data
