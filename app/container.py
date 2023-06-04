from app.dao.redis import RedisDAO
from app.dao.task import TaskDAO
from app.dao.user import UserDAO
from app.services.authentication import AuthenticationService
from app.services.task import TaskService
from app.services.user import UserService

user_dao = UserDAO()
user_service = UserService(user_dao)

task_dao = TaskDAO()
task_service = TaskService(task_dao)

redis_dao = RedisDAO()
auth_service = AuthenticationService(redis_dao)
