import asyncio
from asyncio import AbstractEventLoop, gather

from chalicelib.business.event.dto.request import EventRequestDto
from chalicelib.business.event.dto.response import (
    EventBrandResponseDto,
    EventDetailResponseDto,
    EventSimpleResponseDto,
    EventsResponseDto,
)
from chalicelib.business.interface.business import EventBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    EventServiceIfs,
)
from chalicelib.entity.event import EventEntity
from chalicelib.entity.util import ConstantConverter


class AsyncEventBusiness(EventBusinessIfs):
    def __init__(
        self,
        event_service: EventServiceIfs,
        constant_brand_service: ConstantBrandServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__event_service = event_service
        self.__constant_brand_service = constant_brand_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__event_service, EventServiceIfs)
        assert isinstance(self.__constant_brand_service, ConstantBrandServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_list(self, request: EventRequestDto) -> EventsResponseDto:
        entity: EventEntity = self.__converter.convert_to_entity(request)
        brand_info = ConstantConverter.convert_brand_id(entity.brand)

        event_future = self.__event_service.find_all_by_brand(id=entity.brand)
        constant_brand_future = self.__constant_brand_service.find_all()
        event_entities, constant_brand_entities = self.__loop.run_until_complete(
            gather(event_future, constant_brand_future)
        )
        event_responses = [
            self.__converter.convert_to_dto(e, EventSimpleResponseDto)
            for e in event_entities
        ]

        constant_brand_responses = [
            EventBrandResponseDto(slug=b.slug, name=b.name, image=b.image)
            for b in constant_brand_entities
        ]
        response = EventsResponseDto(
            events=event_responses,
            brands=constant_brand_responses,
            brand_name=brand_info["name"],
            brand_slug=brand_info["slug"],
        )
        return response

    def get_detail(self, request: EventRequestDto) -> EventDetailResponseDto:
        entity = self.__converter.convert_to_entity(request)
        entity = self.__loop.run_until_complete(self.__event_service.find_by_id(entity))
        response = self.__converter.convert_to_dto(entity, EventDetailResponseDto)
        return response
