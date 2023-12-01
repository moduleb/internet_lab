import base64
import hashlib
from fastapi import HTTPException


from app.config.config import config
from app.logger import log


def hash_pass(password: str) -> bytes:
        """
        Хеширует пароль с помощью и возвращает его в виде строки байтов.
        """
        try:
                hash_digest = hashlib.pbkdf2_hmac(
                        hash_name= config.password.ALGORITHM,
                        password= password.encode('utf-8'),
                        salt= config.password.SALT.encode('utf-8'),
                        iterations= config.password.ITERATIONS
                )
                return base64.b64encode(hash_digest).decode('utf-8')


        except Exception as e:
                log.error(f'Ошибка хеширования пароля: {e}')
                raise HTTPException(500, detail="Ошибка хеширования пароля")

