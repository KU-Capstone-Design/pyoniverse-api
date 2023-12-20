import pytest
from chalice import BadRequestError

from chalicelib.business.search.business import AsyncSearchBusiness
from chalicelib.business.search.dto.request import SearchResultRequestDto
from chalicelib.business.search.dto.response import (
    SearchHomeResponseDto,
    SearchResultResponseDto,
)
from chalicelib.converter.search import SearchConverter


def test_search_business(
    constant_brand_service, product_service, search_service, event_loop
):
    # given
    business = AsyncSearchBusiness(
        constant_brand_service=constant_brand_service,
        product_service=product_service,
        search_service=search_service,
        converter=SearchConverter(),
        loop=event_loop,
    )
    # when
    index = business.get_index()
    # then
    assert isinstance(index, SearchHomeResponseDto)


def test_search(constant_brand_service, product_service, search_service, event_loop):
    # given
    business = AsyncSearchBusiness(
        constant_brand_service=constant_brand_service,
        product_service=product_service,
        search_service=search_service,
        converter=SearchConverter(),
        loop=event_loop,
    )
    request = SearchResultRequestDto(
        query="우유",
    )
    # when
    res = business.get_result(request=request)
    # then
    assert isinstance(res, SearchResultResponseDto)
    for product in res.products:
        assert product.price != product.event_price
        if product.event_price is not None:
            assert product.event_price < product.price
    assert res.products_count == len(res.products)

    assert sorted(res.categories, key=lambda x: x.id) == res.categories
    assert sorted(res.brands, key=lambda x: x.id) == res.brands
    assert sorted(res.events, key=lambda x: x.id) == res.events


def test_search_request_validator():
    tmp_data = {
        "invalid_query": 1,
    }
    with pytest.raises(BadRequestError) as e:
        SearchResultRequestDto.validate(tmp_data)

    request = SearchResultRequestDto.load({"query": ""})
    assert request.page == 1
    assert request.page_size == 10
    assert request.query == ""
    assert request.sort_key == "event_price"
    assert request.sort_direction == "asc"
