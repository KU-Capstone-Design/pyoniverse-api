from chalicelib.view.model.api import Api
from tests.schema.metric.metric_response import MetricResponseSchema


def test_spec_get_good_count(env, test_client, event_loop):
    import json

    res = test_client.http.get("/v1/metric/good?domain=product&id=1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(MetricResponseSchema, body, many=False) == {}


def test_spec_get_view_count(env, test_client, event_loop):
    import json

    res = test_client.http.get("/v1/metric/view?domain=product&id=1")
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(MetricResponseSchema, body, many=False) == {}


def test_spec_update_good_count(env, test_client, event_loop):
    import json

    res = test_client.http.patch(
        "/v1/metric/good",
        headers={"Content-Type": "application/json"},
        body=json.dumps({"domain": "product", "id": 1, "value": 0}),
    )
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(MetricResponseSchema, body, many=False) == {}


def test_spec_update_view_count(env, test_client, event_loop):
    import json

    res = test_client.http.patch(
        "/v1/metric/view",
        headers={"Content-Type": "application/json"},
        body=json.dumps({"domain": "product", "id": 1, "value": 0}),
    )
    body = json.loads(res.body)
    assert res.status_code == 200
    assert Api.validate(MetricResponseSchema, body, many=False) == {}
