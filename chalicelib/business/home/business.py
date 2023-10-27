from asyncio import AbstractEventLoop

from chalice import BadRequestError

from chalicelib.business.home.dto.request import HomeRequestDto
from chalicelib.business.home.dto.response import (
    HomeBrandsResponseDto,
    HomeEventsResponseDto,
    HomeProductsResponseDto,
)
from chalicelib.business.interface.business import HomeBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    EventServiceIfs,
    ProductServiceIfs,
)


class AsyncHomeBusiness(HomeBusinessIfs):
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

    def get_list(
        self, request: HomeRequestDto
    ) -> HomeEventsResponseDto | HomeProductsResponseDto | HomeBrandsResponseDto:
        match request.type:
            case "events":
                entities = self.__event_service.find_chunk(
                    sort_key="good_count",
                    direction="desc",
                    chunk_size=5,
                )
                response = list(
                    map(
                        self.__converter.convert_to_dto,
                        self.__loop.run_until_complete(entities),
                    )
                )
                result = HomeEventsResponseDto(events=response)
            case "products":
                entities = self.__product_service.find_chunk(
                    sort_key="good_count",
                    direction="desc",
                    chunk_size=6,
                )
                response = list(
                    map(
                        self.__converter.convert_to_dto,
                        self.__loop.run_until_complete(entities),
                    )
                )
                result = HomeProductsResponseDto(products=response)
            case "stores":
                entities = self.__constant_brand_service.find_all()
                response = list(
                    map(
                        self.__converter.convert_to_dto,
                        self.__loop.run_until_complete(entities),
                    )
                )
                result = HomeBrandsResponseDto(stores=response)
            case _:
                raise BadRequestError(
                    f"{request.type} shoud be in ['events', 'products', 'stores']"
                )
        return result
