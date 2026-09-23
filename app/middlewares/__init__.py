from flask import Flask
from app.middlewares.exception_handler import register_exception_handler
from app.middlewares.request_tracer import register_request_tracer
from app.utils.jwt_utils import JwtUtils

def register_middlewares(app: Flask, jwt_utils: JwtUtils):
    register_exception_handler(app)
    register_request_tracer(app, jwt_utils)