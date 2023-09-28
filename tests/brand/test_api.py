import pytest

from chalicelib.brand.model.brand_response import BrandDetailResponseSchema
from chalicelib.dtos.api import ApiSchema
from chalicelib.home.model.event_response import HomeEventResponseSchema
from chalicelib.home.model.product_response import HomeProductResponseSchema
from chalicelib.home.model.store_response import HomeStoreResponseSchema


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


@pytest.fixture()
def headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip",
    }


def test_spec_store(env, headers):
    from app import app
    import json
    import gzip
    from chalice.test import Client

    with Client(app, stage_name="dev_v1") as client:
        res = client.http.get("/v1/brand/cu", headers=headers)
        body = json.loads(gzip.decompress(res.body).decode("utf-8"))
        assert res.status_code == 200
        assert ApiSchema.get_schema(BrandDetailResponseSchema).validate(body) == {}
