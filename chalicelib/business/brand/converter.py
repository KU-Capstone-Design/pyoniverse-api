from typing import Type

from chalice import BadRequestError

from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import (
    BrandEventResponseDto,
    BrandMetaResponseDto,
    BrandProductResponseDto,
    BrandResponseDto,
)
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.entity.brand import BrandEntity


class BrandConverter(ConverterIfs):
    def convert_to_dto(
        self, entity: BrandEntity, dto_type: Type[DtoType] = BrandResponseDto
    ) -> BrandResponseDto:
        if not isinstance(entity, BrandEntity):
            raise BadRequestError("Entity must be BrandEntity")
        return BrandResponseDto(
            id=entity.id,
            slug=entity.slug,
            name=entity.name,
            meta=BrandMetaResponseDto(description=entity.meta.description),
            description=entity.description,
            events=[
                BrandEventResponseDto(
                    brand=e.brand,
                    image=e.image,
                    name=e.name,
                    id=e.id,
                    image_alt=e.image_alt,
                    start_at=e.start_at,
                    end_at=e.end_at,
                    good_count=e.good_count,
                    view_count=e.view_count,
                )
                for e in entity.events
            ],
            products=[
                BrandProductResponseDto(
                    id=p.id,
                    image=p.image,
                    image_alt=p.image_alt,
                    name=p.name,
                    good_count=p.good_count,
                    view_count=p.view_count,
                    price=p.price,
                    events=p.events,
                    event_price=p.event_price,
                )
                for p in entity.products
            ],
            image=entity.image,
            image_alt=entity.image_alt,
        )

    def convert_to_entity(self, dto: BrandRequestDto) -> BrandEntity:
        if not isinstance(dto, BrandRequestDto):
            raise BadRequestError("dto must be BrandRequestDto")
        return BrandEntity(
            slug=dto.slug,
        )
