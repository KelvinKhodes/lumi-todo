from app.repositories.user_repo import UserRepository
from app.repositories.lecturer_repo import LecturerRepository
from app.repositories.course_repo import CourseRepository
from app.repositories.course_task_repo import CourseTaskRepository

from app.services.user_service import UserService
from app.services.lecturer_service import LecturerService
from app.services.course_service import CourseService
from app.services.course_task_service import CourseTaskService
from app.services.authentication_service import AuthenticationService

from app.cores.extensions import db
from app.utils.jwt_utils import JwtUtils
from app.utils.password_hasher import PasswordHasher
from argon2 import PasswordHasher as ArgonPasswordHasher
from app import Config

class Container:
    def __init__(self):
        # Utils
        self.user_password_hash = PasswordHasher(ArgonPasswordHasher())
        self.session = db.session
        self.jwt_utils = JwtUtils(Config.SECRET_KEY)

        # Repositories
        self.user_repo = UserRepository(self.session)
        self.lecturer_repo = LecturerRepository(self.session)
        self.course_repo = CourseRepository(self.session)
        self.course_task_repo = CourseTaskRepository(self.session)

        # Services
        self.course_service = CourseService(self.course_repo, self.lecturer_repo, self.session)
        self.user_service = UserService(self.user_repo, self.user_password_hash, self.session)
        self.lecturer_service = LecturerService(self.lecturer_repo, self.session)
        self.course_task_service = CourseTaskService(self.course_task_repo, self.course_repo, self.session)
        self.authentication_service = AuthenticationService(self.user_repo, self.user_password_hash, self.jwt_utils, self.session)