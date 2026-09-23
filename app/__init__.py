from flask import Flask
from flasgger import Swagger
from app.cores.config import Config
from app.cores.extensions import db, migrate
from app.cores.container import Container
from app.cores.swagger import build_swagger_template
from app.routes.user_route import create_user_bp
from app.routes.lecturer_route import create_lecturer_bp
from app.routes.course_route import create_course_bp
from app.routes.course_task_route import create_course_task_bp
from app.routes.authentication_route import create_authentication_bp

from app.middlewares import register_middlewares
from app.cores.logging import configure_logger
from app.models.user import User
from app.models.lecturer import Lecturer
from app.models.course import Course
from app.models.course_task import CourseTask
from app.models.enums.task_status import TaskStatus

def create_app():
    configure_logger(environment=Config.APP_ENVIRONMENT)
    app = Flask(__name__)

    app.config.from_object(Config)
    Swagger(app, template=build_swagger_template())
    db.init_app(app)
    migrate.init_app(app, db)

    container = Container()
    
    app.register_blueprint(create_user_bp(container.user_service))
    app.register_blueprint(create_lecturer_bp(container.lecturer_service))
    app.register_blueprint(create_course_bp(container.course_service))
    app.register_blueprint(create_course_task_bp(container.course_task_service))
    app.register_blueprint(create_authentication_bp(container.authentication_service))

    register_middlewares(app, container.jwt_utils)
    return app