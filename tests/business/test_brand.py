from chalicelib.business.brand.business import AsyncBrandBusiness
from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import BrandResponseDto
from chalicelib.converter.brand import BrandConverter
from chalicelib.entity.brand import BrandEntity


def test_brand_business(
    constant_brand_service, product_service, event_service, event_loop
):
    # given
    business = AsyncBrandBusiness(
        constant_brand_service=constant_brand_service,
        product_service=product_service,
        event_service=event_service,
        converter=BrandConverter(),
        loop=event_loop,
    )
    # when
    result = business.get_detail_page(request=BrandRequestDto(slug="cu"))
    # then
    assert isinstance(result, BrandResponseDto)


def test_brand_converter():
    # given
    converter = BrandConverter()
    request = BrandRequestDto(slug="cu")
    # when & then
    entity = converter.convert_to_entity(request)
    assert isinstance(entity, BrandEntity) and entity.slug == request.slug

    response = converter.convert_to_dto(entity)
    assert isinstance(response, BrandResponseDto)
