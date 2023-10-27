from datetime import datetime
from typing import Type

from chalice import BadRequestError

from chalicelib.business.home.dto.request import HomeRequestDto
from chalicelib.business.home.dto.response import (
    HomeBrandResponseDto,
    HomeEventResponseDto,
    HomeProductResponseDto,
)
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.entity.base import EntityType
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity
from chalicelib.entity.util import ConstantConverter


class HomeConverter(ConverterIfs):
    def convert_to_entity(self, dto: HomeRequestDto) -> EntityType:
        raise NotImplementedError

    def convert_to_dto(
        self,
        entity: ConstantBrandEntity | ProductEntity | EventEntity,
        dto_type: Type[DtoType] = None,
    ) -> HomeBrandResponseDto | HomeProductResponseDto | HomeEventResponseDto:
        if isinstance(entity, ConstantBrandEntity):
            return HomeBrandResponseDto(
                image=entity.image,
                image_alt=f"{entity.name.upper()} Logo",
                name=entity.name,
                brand=entity.name.upper(),
                slug=entity.slug,
            )
        elif isinstance(entity, EventEntity):
            brand = ConstantConverter.convert_brand_id(entity.brand)["name"].upper()
            start_at = datetime.fromtimestamp(entity.start_at).strftime("%Y-%m-%d")
            end_at = datetime.fromtimestamp(entity.end_at).strftime("%Y-%m-%d")
            return HomeEventResponseDto(
                image=entity.image.thumb,
                image_alt=f"({brand}) {entity.name}",
                name=entity.name,
                id=entity.id,
                brand=brand,
                start_at=start_at,
                end_at=end_at,
            )
        elif isinstance(entity, ProductEntity):
            events = [
                ConstantConverter.convert_event_id(e)["name"]
                for e in entity.best.events
            ]
            event_brand = ConstantConverter.convert_brand_id(entity.best.brand)[
                "name"
            ].upper()
            event_price = (
                entity.best.price if entity.best.price < entity.price else None
            )
            image_alt = f"{entity.name} thumbnail"
            return HomeProductResponseDto(
                image=entity.image,
                image_alt=image_alt,
                name=entity.name,
                id=entity.id,
                events=events,
                price=entity.price,
                event_price=event_price,
                event_brand=event_brand,
                good_count=entity.good_count,
            )

        else:
            raise BadRequestError(
                f"{entity} should be in ['ConstantBrandEntity', 'ProductEntity', 'EventEntity']"
            )
