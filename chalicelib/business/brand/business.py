from asyncio import AbstractEventLoop

from chalice import BadRequestError

from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import BrandResponseDto
from chalicelib.business.interface.business import BusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import BrandServiceIfs


class AsyncBrandBusiness(BusinessIfs):
    def __init__(
        self,
        brand_service: BrandServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__brand_service = brand_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__brand_service, BrandServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_detail_page(self, request: BrandRequestDto) -> BrandResponseDto:
        if not isinstance(request, BrandRequestDto):
            raise BadRequestError(f"{request} should be BrandRequestDto type")
        if not isinstance(request.id, int):
            raise BadRequestError(f"{request.id} should be int type")
        entity = self.__converter.convert_to_entity(request)
        entity = self.__loop.run_until_complete(self.__brand_service.find_by_id(entity))
        response = self.__converter.convert_to_dto(entity)
        return response
