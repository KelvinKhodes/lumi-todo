from flask import Flask
from app.exceptions.base_exception import BaseException
from app.exceptions.resource_missing import ResourceMissing
from app.exceptions.duplicate_entity import DuplicateEntity
from app.exceptions.authentication_exception import AuthenticationException

from app.routes.wrapper.response_wrapper import wrap_error


def register_exception_handler(app: Flask):

    @app.errorhandler(ResourceMissing)
    def handle_resource_missing(error: BaseException):
        return wrap_error(error), error.status_code

    @app.errorhandler(DuplicateEntity)
    def handle_duplicate_entity(error: BaseException):
            return wrap_error(error), error.status_code

    @app.errorhandler(AuthenticationException)
    def handle_authentication_exception(error: BaseException):
        return wrap_error(error), error.status_code