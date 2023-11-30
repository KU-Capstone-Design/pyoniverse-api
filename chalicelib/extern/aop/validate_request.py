from functools import wraps
from typing import Any, Callable, Mapping, Type

from chalice import BadRequestError
from marshmallow import Schema


def validate_request(schema: Type[Schema]):
    def __validate_request(controller: Callable[[Mapping], Any]):
        @wraps(controller)
        def wrapper(request: Mapping) -> Any:
            """
            :param request: Request Body
            """
            errors = schema().validate(request)
            if errors:
                raise BadRequestError(f"잘못된 요청입니다\n{errors}")
            res = controller(request)
            return res

        return wrapper

    return __validate_request
