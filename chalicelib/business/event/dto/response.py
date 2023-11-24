from dataclasses import dataclass, field
from typing import List

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class EventDetailResponseDto(DtoIfs):
    id: int = field(default=None)
    name: str = field(default=None)
    brand_slug: str = field(default=None)
    brand_name: str = field(default=None)
    view_count: int = field(default=None)
    good_count: int = field(default=None)
    images: List[str] = field(default_factory=list)
    image_alt: str = field(default=None)
    start_at: str = field(default=None)
    end_at: str = field(default=None)


@dataclass(kw_only=True)
class EventSimpleResponseDto(DtoIfs):
    id: int = field(default=None)
    name: str = field(default=None)
    start_at: str = field(default=None)
    end_at: str = field(default=None)
    image: str = field(default=None)
    image_alt: str = field(default=None)
    view_count: int = field(default=None)
    good_count: int = field(default=None)


@dataclass(kw_only=True)
class EventBrandResponseDto:
    slug: str = field(default=None)
    name: str = field(default=None)
    image: str = field(default=None)


@dataclass(kw_only=True)
class EventsResponseDto(DtoIfs):
    brands: List[EventBrandResponseDto] = field(default_factory=list)
    brand_slug: str = field(default=None)
    brand_name: str = field(default=None)
    events: List[EventSimpleResponseDto] = field(default_factory=list)
