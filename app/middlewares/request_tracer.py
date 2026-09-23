from flask import Flask, request, g
from app.exceptions.authentication_exception import AuthenticationException
import structlog
import uuid
from app.utils.jwt_utils import JwtUtils

PUBLIC_PATHS = {
    "authentications", 
    "users",
    "apidocs",
    "flasgger_static"
    }

def register_request_tracer(app: Flask, jwt_utils: JwtUtils):

    @app.before_request
    def add_auth_context():
        print(request.path.rsplit("/"))
        if request.path.rsplit("/")[1] in PUBLIC_PATHS or request.path.__contains__("apispec"):
            return
        
        bearer = request.headers.get("Authorization")

        if bearer is None:
            raise AuthenticationException("Access Token at header 'Authorization' is missing!")
        token = bearer.split("Bearer ")[1]

        payload = jwt_utils.verify(token)
        g.user_id = payload.get("sub")

    @app.before_request
    def add_request_id_to_context():
        structlog.contextvars.clear_contextvars()

        request_id = uuid.uuid4()
        g.request_id = request_id
        
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.path,
            method=request.method
        )

    @app.teardown_request
    def delete_request_id_from_context(exception = None):
        structlog.contextvars.clear_contextvars()