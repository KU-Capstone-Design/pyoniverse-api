from chalicelib.domain.event.model.event_detail_response import (
    EventDetailResponseSchema,
)
from chalicelib.domain.event.model.event_list_response import EventListResponseSchema
from chalicelib.domain.home.model.event_response import HomeEventResponseSchema
from chalicelib.domain.home.model.product_response import HomeProductResponseSchema
from chalicelib.domain.home.model.store_response import HomeStoreResponseSchema
from chalicelib.models.api import ApiSchema
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

    res = test_client.http.get("/v1/events/gs25", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventListResponseSchema).validate(body) == {}
    assert res["data"]["brand_slug"] == "gs25"


def test_spec_event_detail(env, test_client, headers):
    import json
    import gzip

    res = test_client.http.get("/v1/event/1", headers=headers)
    body = json.loads(gzip.decompress(res.body).decode("utf-8"))
    assert res.status_code == 200
    assert ApiSchema.get_schema(EventDetailResponseSchema).validate(body) == {}
