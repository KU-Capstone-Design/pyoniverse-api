import pytest

from chalicelib.extern.dependency_injector.injector import MainInjector


@pytest.fixture
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


@pytest.fixture
def test_client(env):
    from chalice.test import Client
    from app import app

    with Client(app, stage_name="test") as client:
        yield client


@pytest.fixture
def injector(env, event_loop):
    injector = MainInjector()
    injector.inject()
