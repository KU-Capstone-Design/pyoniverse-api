from chalicelib.business.interface.business import ProductBusinessIfs
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import ProductResponseDto


class AsyncProductBusiness(ProductBusinessIfs):
    def get_detail(self, request: ProductRequestDto) -> ProductResponseDto:
        pass
