import redis

from app.config import config

# Подключаемся к Redis
r = redis.Redis(host=config.redis.HOST,
                port=config.redis.PORT,
                db=0)