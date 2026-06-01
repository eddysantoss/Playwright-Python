import os

import pytest
from dotenv import load_dotenv

load_dotenv(override=True)

@pytest.fixture
def credentials():
    return {
        "username": os.getenv("TEST_USERNAME", "Admin"),
        "password": os.getenv("TEST_PASSWORD", "admin123"),
    }
