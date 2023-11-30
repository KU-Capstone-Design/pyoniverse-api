from dataclasses import dataclass, field
from typing import List

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class SearchHomeResponseDto(DtoIfs):
    recommendations: List[str] = field(default_factory=list)
    histories: List[str] = field(default_factory=list)


@dataclass(kw_only=True)
class SearchResultCategoryResponseDto:
    id: int | None = field(default=None)
    name: str = field(default=None)


@dataclass(kw_only=True)
class SearchResultEventResponseDto:
    id: int | None = field(default=None)
    name: str = field(default=None)


@dataclass(kw_only=True)
class SearchResultBrandResponseDto:
    id: int | None = field(default=None)
    name: str = field(default=None)
    image: str | None = field(default=None)


@dataclass(kw_only=True)
class SearchResultProductResponseDto:
    id: int = field(default=None)
    name: str = field(default=None)
    image: str = field(default=None)
    image_alt: str = field(default=None)
    price: float = field(default=None)
    events: List[str] = field(default_factory=list)
    event_price: float | None = field(default=None)
    category: int | None = field(default=None)
    brands: List[int] = field(default_factory=list)


@dataclass(kw_only=True)
class SearchResultResponseMetaDto(DtoIfs):
    current_page: int
    total_page: int
    current_size: int
    page_size: int
    total_size: int
    sort_key: str
    sort_direction: str


@dataclass(kw_only=True)
class SearchResultResponseDto(DtoIfs):
    categories: List[SearchResultCategoryResponseDto] = field(default_factory=list)
    events: List[SearchResultEventResponseDto] = field(default_factory=list)
    brands: List[SearchResultBrandResponseDto] = field(default_factory=list)
    products: List[SearchResultProductResponseDto] = field(default_factory=list)
    products_count: int = field(default=None)
    meta: SearchResultResponseMetaDto = field(
        default_factory=SearchResultResponseMetaDto
    )
