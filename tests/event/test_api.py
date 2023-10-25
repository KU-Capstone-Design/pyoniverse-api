from chalicelib.common.model.api import ApiSchema
from chalicelib.domain.event.model.event_detail_response import (
    EventDetailResponseSchema,
)
from chalicelib.domain.event.model.event_list_response import EventListResponseSchema
from tests.mock.mock import env, test_client


def test_spec_default_event_list(env, test_client):
    import json

    res = test_client.http.get("/v1/events")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventListResponseSchema).validate(body) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_list(env, test_client):
    import json

    res = test_client.http.get("/v1/events/cu")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventListResponseSchema).validate(body) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_detail(env, test_client):
    import json

    res = test_client.http.get("/v1/event/1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventDetailResponseSchema).validate(body) == {}
