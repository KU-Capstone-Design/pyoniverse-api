from dataclasses import dataclass, field
from typing import Any, List

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class HomeBrandResponseDto:
    image: str = field(default=None)
    image_alt: str = field(default=None)
    name: str = field(default=None)
    brand: str = field(default=None)
    slug: str = field(default=None)


@dataclass(kw_only=True)
class HomeBrandsResponseDto(DtoIfs):
    stores: List[HomeBrandResponseDto] = field(default_factory=list)
    search: Any = field(default=None)


@dataclass(kw_only=True)
class HomeProductResponseDto:
    image: str = field(default=None)
    image_alt: str = field(default=None)
    name: str = field(default=None)
    id: int = field(default=None)
    events: List[int] = field(default_factory=list)
    price: float = field(default=None)
    event_price: float = field(default=None)
    event_brand: str = field(default=None)
    good_count: int = field(default=None)


@dataclass(kw_only=True)
class HomeProductsResponseDto(DtoIfs):
    products: List[HomeProductResponseDto] = field(default_factory=list)


@dataclass(kw_only=True)
class HomeEventResponseDto:
    image: str = field(default=None)
    image_alt: str = field(default=None)
    name: str = field(default=None)
    id: int = field(default=None)
    brand: str = field(default=None)
    start_at: str = field(default=None)
    end_at: str = field(default=None)


@dataclass(kw_only=True)
class HomeEventsResponseDto(DtoIfs):
    events: List[HomeEventResponseDto] = field(default_factory=list)
