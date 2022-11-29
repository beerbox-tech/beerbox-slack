"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox api error response
"""

from typing import Any
from typing import Optional

from slackbox.application.api.components.base import APIComponent


class ErrorResponse(APIComponent):
    """API component representing any error"""

    code: str
    data: Optional[Any] = None
    message: str
