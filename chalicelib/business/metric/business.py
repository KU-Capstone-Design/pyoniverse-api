from asyncio import AbstractEventLoop

from chalice import BadRequestError

from chalicelib.business.interface.business import MetricBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    EventServiceIfs,
    ProductServiceIfs,
)
from chalicelib.business.metric.model.request import MetricRequestDto
from chalicelib.business.metric.model.response import MetricResponseDto
from chalicelib.entity.product import ProductEntity


class AsyncMetricBusiness(MetricBusinessIfs):
    def __init__(
        self,
        event_service: EventServiceIfs,
        product_service: ProductServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__event_service = event_service
        self.__product_service = product_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__event_service, EventServiceIfs)
        assert isinstance(self.__product_service, ProductServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_good_count(self, request: MetricRequestDto) -> MetricResponseDto:
        match request.domain:
            case "product":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case "event":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case _:
                raise BadRequestError(
                    f"{request.domain} should be in ['product', 'event']"
                )
        result = MetricResponseDto(
            id=entity.id, domain=request.domain, value=entity.good_count
        )
        return result

    def get_view_count(self, request: MetricRequestDto) -> MetricResponseDto:
        match request.domain:
            case "product":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case "event":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case _:
                raise BadRequestError(
                    f"{request.domain} should be in ['product', 'event']"
                )
        result = MetricResponseDto(
            id=entity.id, domain=request.domain, value=entity.view_count
        )
        return result

    def update_good_count(self, request: MetricRequestDto) -> MetricResponseDto:
        if not isinstance(request.value, int):
            raise BadRequestError(f"{request.value} should be int type")
        match request.domain:
            case "product":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case "event":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case _:
                raise BadRequestError(
                    f"{request.domain} should be in ['product', 'event']"
                )
        # TODO : Message Queue 연결
        updated_good_count = entity.good_count + request.value
        result = MetricResponseDto(
            id=entity.id, domain=request.domain, value=updated_good_count
        )
        return result

    def update_view_count(self, request: MetricRequestDto) -> MetricResponseDto:
        if not isinstance(request.value, int):
            raise BadRequestError(f"{request.value} should be int type")
        match request.domain:
            case "product":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case "event":
                entity = ProductEntity(id=request.id)
                entity: ProductEntity = self.__loop.run_until_complete(
                    self.__product_service.find_one(entity)
                )
            case _:
                raise BadRequestError(
                    f"{request.domain} should be in ['product', 'event']"
                )
        # TODO : Message Queue 연결
        updated_view_count = entity.view_count + request.value
        result = MetricResponseDto(
            id=entity.id, domain=request.domain, value=updated_view_count
        )
        return result
