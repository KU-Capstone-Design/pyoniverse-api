import pytest

from chalicelib.business.metric.business import AsyncMetricBusiness
from chalicelib.business.metric.model.request import MetricRequestDto
from chalicelib.business.metric.model.response import MetricResponseDto
from chalicelib.converter.metric import MetricConverter


def test_product_business_get_good_count(product_service, event_service, event_loop):
    # given
    business = AsyncMetricBusiness(
        product_service=product_service,
        event_service=event_service,
        converter=MetricConverter(),
        loop=event_loop,
    )
    request1 = MetricRequestDto(id=1, domain="product")
    request2 = MetricRequestDto(id=1, domain="event")
    invalid_request = MetricRequestDto(id=1, domain="invalid")
    # when
    response1: MetricResponseDto = business.get_good_count(request1)
    response2: MetricResponseDto = business.get_good_count(request2)
    # then
    assert isinstance(response1, MetricResponseDto) and isinstance(
        response2, MetricResponseDto
    )
    assert (
        response1.id == request1.id
        and response1.domain == request1.domain
        and isinstance(response1.value, int)
    )
    assert (
        response2.id == request2.id
        and response2.domain == request2.domain
        and isinstance(response2.value, int)
    )

    try:
        business.get_good_count(invalid_request)
        assert False
    except Exception:
        assert True


def test_product_business_get_view_count(product_service, event_service, event_loop):
    # given
    business = AsyncMetricBusiness(
        product_service=product_service,
        event_service=event_service,
        converter=MetricConverter(),
        loop=event_loop,
    )
    request1 = MetricRequestDto(id=1, domain="product")
    request2 = MetricRequestDto(id=1, domain="event")
    invalid_request = MetricRequestDto(id=1, domain="invalid")
    # when
    response1: MetricResponseDto = business.get_view_count(request1)
    response2: MetricResponseDto = business.get_view_count(request2)
    # then
    assert isinstance(response1, MetricResponseDto) and isinstance(
        response2, MetricResponseDto
    )
    assert (
        response1.id == request1.id
        and response1.domain == request1.domain
        and isinstance(response1.value, int)
    )
    assert (
        response2.id == request2.id
        and response2.domain == request2.domain
        and isinstance(response2.value, int)
    )

    try:
        business.get_view_count(invalid_request)
        assert False
    except Exception:
        assert True


def test_product_business_update_good_count(product_service, event_service, event_loop):
    # given
    business = AsyncMetricBusiness(
        product_service=product_service,
        event_service=event_service,
        converter=MetricConverter(),
        loop=event_loop,
    )
    request1 = MetricRequestDto(id=1, domain="product", value=1)
    request2 = MetricRequestDto(id=1, domain="event", value=-1)
    invalid_request1 = MetricRequestDto(id=1, domain="invalid", value=3)
    invalid_request2 = MetricRequestDto(id=1, domain="event", value=None)
    # when
    response1: MetricResponseDto = business.update_good_count(request1)
    response2: MetricResponseDto = business.update_good_count(request2)
    # then
    assert isinstance(response1, MetricResponseDto) and isinstance(
        response2, MetricResponseDto
    )
    assert response1.id == request1.id and response1.domain == request1.domain
    assert response2.id == request2.id and response2.domain == request2.domain

    with pytest.raises(Exception):
        business.update_view_count(invalid_request1)
        business.update_view_count(invalid_request2)


def test_product_business_update_view_count(product_service, event_service, event_loop):
    # given
    business = AsyncMetricBusiness(
        product_service=product_service,
        event_service=event_service,
        converter=MetricConverter(),
        loop=event_loop,
    )
    request1 = MetricRequestDto(id=1, domain="product", value=1)
    request2 = MetricRequestDto(id=1, domain="event", value=-1)
    invalid_request1 = MetricRequestDto(id=1, domain="invalid", value=3)
    invalid_request2 = MetricRequestDto(id=1, domain="event", value=None)
    # when
    response1: MetricResponseDto = business.update_view_count(request1)
    response2: MetricResponseDto = business.update_view_count(request2)
    # then
    assert isinstance(response1, MetricResponseDto) and isinstance(
        response2, MetricResponseDto
    )
    assert response1.id == request1.id and response1.domain == request1.domain
    assert response2.id == request2.id and response2.domain == request2.domain

    with pytest.raises(Exception):
        business.update_view_count(invalid_request1)
        business.update_view_count(invalid_request2)
