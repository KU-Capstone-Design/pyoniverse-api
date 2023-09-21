from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProductPriceEntity:
    value: float = field()
    currency: int = field()
    discounted_value: Optional[float] = field(default=None)

    @classmethod
    def from_dict(cls, data):
        return cls(
            value=data["value"],
            currency=data["currency"],
            discounted_value=data["discounted_value"],
        )


@dataclass
class ProductBrandEntity:
    id: int = field()
    price: ProductPriceEntity = field()
    events: List[int] = field()

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            price=ProductPriceEntity.from_dict(data["price"]),
            events=data["events"],
        )


@dataclass
class ProductEntity:
    id: int
    name: str
    category: int
    image: Optional[str]
    description: Optional[str]
    brands: List[ProductBrandEntity]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            image=data["image"],
            description=data["description"],
            brands=[ProductBrandEntity.from_dict(brand) for brand in data["brands"]],
        )
