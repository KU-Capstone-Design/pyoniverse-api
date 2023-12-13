from dataclasses import dataclass, field
from typing import List

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class BrandMetaResponseDto:
    description: str = field(default=None)


@dataclass(kw_only=True)
class BrandEventResponseDto:
    brand: str = field(default=None)
    image: str = field(default=None)
    name: str = field(default=None)
    id: int = field(default=None)
    image_alt: str = field(default=None)
    start_at: str = field(default=None)
    end_at: str = field(default=None)
    good_count: int = field(default=None)
    view_count: int = field(default=None)


@dataclass(kw_only=True)
class BrandProductResponseDto:
    id: int = field(default=None)
    image: str = field(default=None)
    image_alt: str = field(default=None)
    name: str = field(default=None)
    good_count: int = field(default=None)
    view_count: int = field(default=None)
    price: float = field(default=None)
    events: List[int] = field(default=None)
    event_price: float = field(default=None)


@dataclass(kw_only=True)
class BrandResponseDto(DtoIfs):
    id: int = field(default=None)
    slug: str = field(default=None)
    name: str = field(default=None)
    meta: BrandMetaResponseDto = field(default_factory=BrandMetaResponseDto)
    description: str = field(default=None)
    events: List[BrandEventResponseDto] = field(default_factory=list)
    products: List[BrandProductResponseDto] = field(default_factory=list)
    image: str = field(default=None)
    image_alt: str = field(default=None)
