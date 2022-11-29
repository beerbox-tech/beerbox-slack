"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox health resources integration tests
"""


import pytest

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


@pytest.mark.asyncio
async def test_livez(client):
    """test get livez resource"""
    response = client.get("/livez")

    assert response.status_code == 200
    assert response.json() == {
        "checks": [
            {
                "name": "slackbox:ready",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": AnyDatetimeString(),
            }
        ],
        "service": "slackbox",
        "status": "pass",
        "version": AnyInstanceOf(str),
    }


@pytest.mark.asyncio
async def test_readyz(client):
    """test get readyz resource"""
    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json() == {
        "checks": [
            {
                "name": "slackbox:ready",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": AnyDatetimeString(),
            }
        ],
        "service": "slackbox",
        "status": "pass",
        "version": "dev",
    }
