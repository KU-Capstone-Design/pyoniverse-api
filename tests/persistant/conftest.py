import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="package")
def mongo_client(env):
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    client.get_io_loop().run_until_complete(client.admin.command("ping"))
    yield client
    client.close()
