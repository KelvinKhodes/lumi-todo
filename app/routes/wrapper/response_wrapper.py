from flask import Response, jsonify
from pydantic import BaseModel
from typing import Sequence

import structlog
from app.exceptions.base_exception import BaseException

def wrap_data(data: BaseModel) -> Response:
    return jsonify({
        'data': data.model_dump(),
        'errors': None,
        'request_id': structlog.contextvars.get_contextvars().get("request_id", "None")
    })
def wrap_list_data(datas: Sequence[BaseModel]) -> Response:
    return jsonify({
        'data': [data.model_dump() for data in datas],
        'errors': None,
        'request_id': structlog.contextvars.get_contextvars().get("request_id", "None")
    })
def wrap_error(error: BaseException) -> Response:
    return jsonify({
        'data': None,
        'errors': error.message,
        'request_id': structlog.contextvars.get_contextvars().get("request_id", "None")       
    })