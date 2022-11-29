"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox api health response
"""

from __future__ import annotations

from datetime import datetime

from slackbox import config
from slackbox.application.api.components.base import APIComponent
from slackbox.application.health import Check
from slackbox.application.health import Status


class HealthCheck(APIComponent):
    """API component representing a healtch check"""

    name: str
    time: datetime
    status: Status
    observed_value: str
    observed_unit: str

    @classmethod
    def from_check(cls, check: Check) -> HealthCheck:
        """create an api component from a health check"""
        return cls(
            name=check.name,
            time=check.time,
            status=check.status,
            observed_value=check.observed_value,
            observed_unit=check.observed_unit,
        )


class HealthResponse(APIComponent):
    """API component representing a healt check response"""

    status: Status
    checks: list[HealthCheck]
    version: str
    service: str

    @classmethod
    def from_checks(cls, checks: list[Check]) -> HealthResponse:
        """transform a list of application checks into a healtch check response"""
        version = config.VERSION
        service = config.SERVICE
        return cls(
            status=Status.all(check.status for check in checks),
            checks=[HealthCheck.from_check(check) for check in checks],
            version=version,
            service=service,
        )
