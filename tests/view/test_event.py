import pytest

from chalicelib.common.model.api import Api
from chalicelib.dependency_injector.injector import MainInjector
from chalicelib.domain.event.model.event_detail_response import (
    EventDetailResponseSchema,
)
from chalicelib.domain.event.model.event_list_response import EventListResponseSchema
from tests.mock.mock import env, test_client


@pytest.fixture
def injector(env):
    injector = MainInjector()
    injector.inject()


def test_spec_default_event_list(test_client, injector):
    import json

    res = test_client.http.get("/v1/events")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(EventListResponseSchema, body, many=False) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_list(test_client, injector):
    import json

    res = test_client.http.get("/v1/events/cu")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(EventListResponseSchema, body, many=False) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_detail(test_client, injector):
    import json

    res = test_client.http.get("/v1/event/1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(EventDetailResponseSchema, body, many=False) == {}
