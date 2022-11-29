"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox integration tests configuration
"""

import pytest
from fastapi.testclient import TestClient

from slackbox.main import app


@pytest.fixture(name="client", scope="session")
def fixture_client():
    """return a test client"""
    return TestClient(app)
