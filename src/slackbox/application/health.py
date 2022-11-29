"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox applicative health management
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Iterable
from typing import Protocol

from slackbox import config


class Status(Enum):
    """health check status"""

    PASS = "pass"  # nosec: bandit[B105] this is not a password
    FAIL = "fail"

    @classmethod
    def all(cls, statuses: Iterable[Status]) -> Status:
        """aggregate multiple statuses into one"""
        for status in statuses:
            if status is Status.FAIL:
                return Status.FAIL
        return Status.PASS


@dataclass(frozen=True)
class Check:
    """health check data container"""

    name: str
    time: datetime
    status: Status
    observed_value: str
    observed_unit: str


class HealthIndicator(Protocol):
    """protocol to be implemented by any class exposing a health check"""

    def get_check(self) -> Check:
        """method to be implemented exposing the health check"""
        ...


class ApplicationReadiness(HealthIndicator):
    """application readiness health indicator"""

    def get_check(self) -> Check:
        return Check(
            name=f"{config.SERVICE}:ready",
            time=datetime.now(),
            status=Status.PASS,
            observed_value="true",
            observed_unit="boolean",
        )
