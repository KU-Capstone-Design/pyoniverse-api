from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import BrandResponseDto
from chalicelib.business.home.business import AsyncHomeBusiness
from chalicelib.business.home.dto.request import HomeRequestDto
from chalicelib.business.home.dto.response import (
    HomeBrandsResponseDto,
    HomeEventsResponseDto,
    HomeProductsResponseDto,
)
from chalicelib.converter.brand import BrandConverter
from chalicelib.converter.home import HomeConverter
from chalicelib.entity.brand import BrandEntity


def test_home_business(
    constant_brand_service, event_service, product_service, event_loop
):
    # given
    business = AsyncHomeBusiness(
        constant_brand_service=constant_brand_service,
        event_service=event_service,
        product_service=product_service,
        converter=HomeConverter(),
        loop=event_loop,
    )
    # when
    events = business.get_list(request=HomeRequestDto(type="events"))
    products = business.get_list(request=HomeRequestDto(type="products"))
    stores = business.get_list(request=HomeRequestDto(type="stores"))
    # then
    assert isinstance(events, HomeEventsResponseDto)
    assert isinstance(products, HomeProductsResponseDto)
    assert isinstance(stores, HomeBrandsResponseDto)


def test_home_converter():
    # given
    converter = BrandConverter()
    request = BrandRequestDto(slug="cu")
    # when & then
    entity = converter.convert_to_entity(request)
    assert isinstance(entity, BrandEntity) and entity.slug == request.slug

    response = converter.convert_to_dto(entity)
    assert isinstance(response, BrandResponseDto)
