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
    
@pytest.fixture
def invalid_credentials():
    return {
        "username": os.getenv("TEST_INVALID_USERNAME", "invalid_user"),
        "password": os.getenv("TEST_INVALID_PASSWORD", "invalid_pass"),
    }
