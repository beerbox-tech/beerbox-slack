"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

unit testing slackbox api response
"""

from slackbox.application.api.components.base import APIComponent
from slackbox.application.api.response import APIResponse


class Dummy(APIComponent):
    """dummy component to test rendering"""

    dummy: bool


def test_render_single():
    """test the response rendering with a single component"""
    response = APIResponse(content=Dummy(dummy=True), status_code=418)
    assert response.body == b'{"dummy":true}'


def test_render_list():
    """test the response rendering with a single component"""
    response = APIResponse(content=[Dummy(dummy=True), Dummy(dummy=False)], status_code=418)
    assert response.body == b'[{"dummy":true},{"dummy":false}]'
