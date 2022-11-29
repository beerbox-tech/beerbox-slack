"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox api response
"""

from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from slackbox.application.api.components.base import APIComponent


class APIResponse(JSONResponse):
    """API response able to render any API component"""

    def to_data(self, component: APIComponent) -> Any:
        """transfrom a component into serializable data"""
        return component.dict(by_alias=True, exclude_unset=True, exclude_none=True)

    def render(self, content: APIComponent | list[APIComponent]) -> bytes:
        if isinstance(content, list):
            data = [self.to_data(item) for item in content]
        else:
            data = self.to_data(content)
        json_content = jsonable_encoder(data)
        return super().render(json_content)
