import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="package")
def mongo_client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))
