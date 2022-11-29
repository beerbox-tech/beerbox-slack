"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox api exception handlers
"""

from functools import singledispatch
from typing import Any

from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request

from slackbox.application.api.components.error_response import ErrorResponse
from slackbox.application.api.response import APIResponse


@singledispatch
def get_status_code_from(_) -> int:
    """get a HTTP status code from an exception"""
    return status.HTTP_500_INTERNAL_SERVER_ERROR


@get_status_code_from.register
def _(_: RequestValidationError) -> int:
    return status.HTTP_422_UNPROCESSABLE_ENTITY


@get_status_code_from.register
def _(exception: HTTPException) -> int:
    return exception.status_code


@singledispatch
def get_error_code_from(_) -> str:
    """get an error code from an exception"""
    return "internal-error"


@get_error_code_from.register
def _(exception: HTTPException) -> str:
    error_code = exception.detail.lower()
    # avoid ' in raw error code for 418 I'm a Teapot HTTP error
    error_code = error_code.replace("i'm", "i am")
    return error_code.replace(" ", "-")


@get_error_code_from.register
def _(_: RequestValidationError) -> str:
    return "validation-error"


@singledispatch
def get_error_message_from(_) -> str:
    """get an error message from an exception and a request"""
    return "unknown error"


@get_error_message_from.register
def _(exception: HTTPException) -> str:
    if exception.status_code == status.HTTP_404_NOT_FOUND:
        return "requested path does not exist"
    return exception.detail.lower()


@get_error_message_from.register
def _(_: RequestValidationError) -> str:
    return "error validating input data"


@singledispatch
def get_error_data_from(_) -> dict | list[dict] | None:
    """get an error data from an exception"""
    return None


@get_error_data_from.register
def _(exception: RequestValidationError) -> list[dict] | None:
    return [
        {"field": _get_field_from(error["loc"]), "message": error["msg"]}
        for error in exception.errors()
    ]


def _get_field_from(loc: Any) -> str:
    output = f"{loc[0]}"
    for component in loc[1:]:
        if isinstance(component, int):
            output = f"{output}[{component}]"
        else:
            output = f"{output}.{component}"
    return output


async def exception_handler(_: Request, exc: Exception) -> APIResponse:
    """generic handler transforming any exception into an API response"""
    return APIResponse(
        status_code=get_status_code_from(exc),
        content=ErrorResponse(
            code=get_error_code_from(exc),
            message=get_error_message_from(exc),
            data=get_error_data_from(exc),
        ),
    )
