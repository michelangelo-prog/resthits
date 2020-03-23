from functools import wraps

from flask import abort, request
from marshmallow import ValidationError


def request_schema(schema):
    def _verify_schema(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            json = request.get_json()
            try:
                json_data = schema().load(json)
            except ValidationError:
                abort(400)
            return f(json_data, *args, **kwargs)

        return wrapper

    return _verify_schema
