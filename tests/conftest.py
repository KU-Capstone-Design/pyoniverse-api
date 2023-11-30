import asyncio
import os

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.extern.dependency_injector.injector import MainInjector


@pytest.fixture(scope="session")
def env():
    import os

    while "app.py" not in os.listdir():
        os.chdir("..")
    import dotenv

    dotenv.load_dotenv()

    # Load .chalice/config.json
    import json

    with open(".chalice/config.json", "r") as fd:
        config = json.load(fd)

    env = config.get("environment_variables", {})
    env.update(
        config.get("stages", {}).get("dev_v1", {}).get("environment_variables", {})
    )
    os.environ.update(env)
    # Change DB to test
    os.environ["MONGO_DB"] = "test"


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client(env):
    return AsyncIOMotorClient(os.getenv("MONGO_URI"))


@pytest.fixture(scope="function")
def test_client(env):
    from chalice.test import Client
    from app import app

    with Client(app, stage_name="test") as client:
        yield client


@pytest.fixture(scope="function")
def injector(env):
    injector = MainInjector()
    injector.inject()
