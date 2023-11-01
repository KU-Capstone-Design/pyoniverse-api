from asyncio import AbstractEventLoop

from chalicelib.business.interface.business import ProductBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import ProductServiceIfs
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import ProductResponseDto


class AsyncProductBusiness(ProductBusinessIfs):
    def __init__(
        self,
        product_service: ProductServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__product_service = product_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__product_service, ProductServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_detail(self, request: ProductRequestDto) -> ProductResponseDto:
        entity = self.__converter.convert_to_entity(request)
        entity = self.__product_service.find_one(entity)
        response = self.__converter.convert_to_dto(entity)
        # TODO : brands 처리
        return response
