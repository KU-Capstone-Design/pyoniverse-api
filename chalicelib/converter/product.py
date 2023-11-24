from typing import Type

from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import ProductResponseDto
from chalicelib.entity.product import ProductEntity


class ProductConverter(ConverterIfs):
    def convert_to_entity(self, dto: ProductRequestDto) -> ProductEntity:
        return ProductEntity(id=dto.id)

    def convert_to_dto(
        self, entity: ProductEntity, dto_type: Type[DtoType] = ProductResponseDto
    ) -> ProductResponseDto:
        # brands는 business에서 처리한다.
        image_alt = f"{entity.name} image"
        return ProductResponseDto(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            image=entity.image,
            image_alt=image_alt,
            best_brand=entity.best.brand,
            good_count=entity.good_count,
            view_count=entity.view_count,
        )
