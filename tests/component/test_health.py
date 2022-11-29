"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

testing slackbox health resources behaviour
"""

import requests

from tests.utils import AnyDatetimeString
from tests.utils import AnyInstanceOf


def test_livez(host, port):
    """test the /livez endpoint"""
    url = f"http://{host}:{port}/livez"

    response = requests.get(url, timeout=1)

    assert response.status_code == 200
    assert response.json() == {
        "checks": [
            {
                "name": "slackbox:ready",
                "observedUnit": "boolean",
                "observedValue": "true",
                "status": "pass",
                "time": AnyDatetimeString(),
            },
        ],
        "service": "slackbox",
        "status": "pass",
        "version": AnyInstanceOf(str),
    }


def test_readyz(host, port):
    """test the /readyz endpoint"""
    url = f"http://{host}:{port}/readyz"

    response = requests.get(url, timeout=1)

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
