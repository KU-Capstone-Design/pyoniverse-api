from asyncio import AbstractEventLoop

from chalicelib.business.home.dto.request import HomeRequestDto
from chalicelib.business.home.dto.response import HomeResponseDto
from chalicelib.business.interface.business import HomeBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    EventServiceIfs,
    ProductServiceIfs,
)


class HomeBusiness(HomeBusinessIfs):
    def __init__(
        self,
        constant_brand_service: ConstantBrandServiceIfs,
        event_service: EventServiceIfs,
        product_service: ProductServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__constant_brand_service = constant_brand_service
        self.__event_service = event_service
        self.__product_service = product_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__constant_brand_service, ConstantBrandServiceIfs)
        assert isinstance(self.__event_service, EventServiceIfs)
        assert isinstance(self.__product_service, ProductServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_list(self, request: HomeRequestDto) -> HomeResponseDto:
        pass
