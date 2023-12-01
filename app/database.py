import mysql
from mysql.connector import OperationalError

from app.config import config
from app.logger import log


try:
    db = mysql.connector.connect(
        host=config.db.HOST,
        user=config.db.USER_NAME,
        password=config.db.PASSWORD,
        database=config.db.DB_NAME,
    )
except Exception as e:
    log.error(f'DB connection error {e}')


def get_cursor():
    try:
        cursor = db.cursor()
        yield cursor
    except OperationalError as e:
        log.error(f"Ошибка подключения к базе данных: {e}")
    finally:
        db.commit()
        cursor.close()
