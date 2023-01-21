"""
created by: Thibault DEFEYTER
created at: 2023/01/22
license: MIT

slackbox slack resources
"""


from fastapi import APIRouter
from fastapi import Request
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

from slackbox.domain.slack import app

router = APIRouter()
handler = AsyncSlackRequestHandler(app)


@router.post("/slack/events")
async def endpoint(request: Request):
    """slack event resource controller"""
    return await handler.handle(request)
