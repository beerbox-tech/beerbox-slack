"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox api health resources
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from slackbox.application.api.components.health_response import HealthResponse
from slackbox.application.api.response import APIResponse
from slackbox.application.health import ApplicationReadiness
from slackbox.application.health import HealthIndicator

router = APIRouter()


def get_application_readiness() -> HealthIndicator:
    """return an application readiness indicator"""
    return ApplicationReadiness()


@router.get("/readyz")
async def get_readyz(
    application_ready: HealthIndicator = Depends(get_application_readiness),
) -> APIResponse:
    """readyz resource controller"""
    checks = [application_ready.get_check()]
    response = HealthResponse.from_checks(checks)
    return APIResponse(content=response, status_code=status.HTTP_200_OK)


@router.get("/livez")
async def get_livez(
    application_ready: HealthIndicator = Depends(get_application_readiness),
) -> APIResponse:
    """livez resource controller"""
    checks = [application_ready.get_check()]
    response = HealthResponse.from_checks(checks)
    return APIResponse(content=response, status_code=status.HTTP_200_OK)
