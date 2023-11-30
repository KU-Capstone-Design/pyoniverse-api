from chalicelib.view.model.api import Api
from tests.mock.mock import env, test_client
from tests.schema.event.event_detail_response import EventDetailResponseSchema
from tests.schema.event.event_list_response import EventListResponseSchema


def test_spec_default_event_list(env, test_client):
    import json

    res = test_client.http.get("/v1/events")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(EventListResponseSchema, body, many=False) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_list(env, test_client):
    import json

    res = test_client.http.get("/v1/events/cu")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(EventListResponseSchema, body, many=False) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_detail(env, test_client):
    import json

    res = test_client.http.get("/v1/event/1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(EventDetailResponseSchema, body, many=False) == {}
