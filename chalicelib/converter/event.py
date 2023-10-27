from datetime import datetime
from typing import Type

from chalice import BadRequestError

from chalicelib.business.event.dto.request import EventRequestDto
from chalicelib.business.event.dto.response import (
    EventDetailResponseDto,
    EventSimpleResponseDto,
)
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.entity.event import EventEntity
from chalicelib.entity.util import ConstantConverter


class EventConverter(ConverterIfs):
    def convert_to_entity(self, dto: EventRequestDto) -> EventEntity:
        return EventEntity(
            id=dto.id, brand=ConstantConverter.convert_brand_slug(dto.brand_slug)
        )

    def convert_to_dto(
        self, entity: EventEntity, dto_type: Type[DtoType]
    ) -> EventDetailResponseDto | EventSimpleResponseDto:
        if dto_type is EventSimpleResponseDto:
            start_at = datetime.fromtimestamp(entity.start_at).strftime("%Y-%m-%d")
            end_at = datetime.fromtimestamp(entity.end_at).strftime("%Y-%m-%d")
            image_alt = f"{entity.name} thumbnail"
            return EventSimpleResponseDto(
                id=entity.id,
                name=entity.name,
                start_at=start_at,
                end_at=end_at,
                image=entity.image.thumb,
                image_alt=image_alt,
                view_count=entity.view_count,
                good_count=entity.good_count,
            )
        elif dto_type is EventDetailResponseDto:
            brand_info = ConstantConverter.convert_brand_id(entity.brand)
            start_at = datetime.fromtimestamp(entity.start_at).strftime("%Y-%m-%d")
            end_at = datetime.fromtimestamp(entity.end_at).strftime("%Y-%m-%d")
            image_alt = f"{entity.name} images"
            return EventDetailResponseDto(
                id=entity.id,
                name=entity.name,
                brand_slug=brand_info["slug"],
                brand_name=brand_info["name"],
                view_count=entity.view_count,
                good_count=entity.good_count,
                images=[entity.image.thumb] + entity.image.others,
                image_alt=image_alt,
                start_at=start_at,
                end_at=end_at,
            )
        else:
            raise BadRequestError(
                f"{dto_type} should be in ['EventsResponseDto', 'EventDetailResponseDto']"
            )
