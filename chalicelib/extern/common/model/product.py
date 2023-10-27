from dataclasses import dataclass, field
from typing import List, Optional

from chalicelib.extern.common.model.converter import IdConverter
from chalicelib.entity.product import (
    ProductBrandEntity,
    ProductEntity,
    ProductPriceEntity,
)


@dataclass
class ProductEventDto:
    id: int = field()
    name: str = field()
    slug: str = field()

    @classmethod
    def from_dict(cls, data: int):
        event_info = IdConverter.convert_event_id(data)
        return cls(
            id=data,
            name=event_info["name"],
            slug=event_info["slug"],
        )


@dataclass
class ProductPriceDto:
    value: float = field()
    currency: str = field()
    discounted_value: Optional[float] = field(default=None)

    @classmethod
    def from_dict(cls, data: ProductPriceEntity):
        currency_info = IdConverter.convert_currency(data.currency)
        return cls(
            value=data.value,
            currency=currency_info["slug"],
            discounted_value=data.discounted_value,
        )


@dataclass
class ProductBrandDto:
    id: int = field()
    slug: str = field()
    name: str = field()
    price: ProductPriceDto = field()
    events: List[ProductEventDto] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: ProductBrandEntity):
        brand_info = IdConverter.convert_brand_id(data.id)
        return cls(
            id=data.id,
            slug=brand_info["slug"],
            name=brand_info["name"],
            price=ProductPriceDto.from_dict(data.price),
            events=[ProductEventDto.from_dict(event) for event in data.events],
        )


@dataclass
class ProductCategoryDto:
    id: int = field()
    name: str = field()
    slug: str = field()

    @classmethod
    def from_dict(cls, data: int):
        category_info = IdConverter.convert_category_id(data)
        return cls(
            id=data,
            name=category_info["name"],
            slug=category_info["slug"],
        )


@dataclass
class ProductDto:
    id: int = field()
    name: str = field()
    category: ProductCategoryDto = field()
    image: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    brands: List[ProductBrandDto] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: ProductEntity):
        return cls(
            id=data.id,
            name=data.name,
            category=ProductCategoryDto.from_dict(data.category),
            image=data.image,
            description=data.description,
            brands=[ProductBrandDto.from_dict(brand) for brand in data.brands],
        )
