from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import ProductResponseDto
from chalicelib.converter.product import ProductConverter


def test_product_converter():
    # given
    converter = ProductConverter()
    request = ProductRequestDto(id=1)
    # when & then
    entity = converter.convert_to_entity(request)
    assert entity.id == request.id
    response = converter.convert_to_dto(entity)
    assert isinstance(response, ProductResponseDto)
