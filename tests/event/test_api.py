from chalicelib.domain.event.model.event_detail_response import (
    EventDetailResponseSchema,
)
from chalicelib.domain.event.model.event_list_response import EventListResponseSchema
from chalicelib.common.model.api import ApiSchema
from tests.mock.mock import test_client, env, headers


def test_spec_default_event_list(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/events", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventListResponseSchema).validate(body) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_list(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/events/cu", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventListResponseSchema).validate(body) == {}
    assert body["data"]["brand_slug"] == "cu"


def test_spec_event_detail(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/event/1", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventDetailResponseSchema).validate(body) == {}