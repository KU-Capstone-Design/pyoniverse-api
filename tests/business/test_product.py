from chalicelib.business.product.business import AsyncProductBusiness
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import ProductResponseDto
from chalicelib.converter.product import ProductConverter


def test_product_business(product_service, constant_brand_service, event_loop):
    # given
    business = AsyncProductBusiness(
        product_service=product_service,
        constant_brand_service=constant_brand_service,
        converter=ProductConverter(),
        loop=event_loop,
    )
    # when
    response: ProductResponseDto = business.get_detail(request=ProductRequestDto(id=1))
    # then
    assert isinstance(response, ProductResponseDto)
    assert response.best_brand in {b.id for b in response.brands}
