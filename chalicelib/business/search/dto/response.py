from dataclasses import dataclass, field
from typing import List, Literal

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
class SearchResultSortResponseDto:
    id: int = field(default=None)
    name: str = field(default=None)


@dataclass(kw_only=True)
class SearchResultSelectedOptionResponseDto:
    category: int | None = field(default=None)
    event: int | None = field(default=None)
    brand: int | None = field(default=None)
    sort: int = field(default=None)
    direction: Literal["asc", "desc"] = field(default=None)


@dataclass(kw_only=True)
class SearchResultProductResponseDto:
    id: int = field(default=None)
    name: str = field(default=None)
    image: str = field(default=None)
    image_alt: str = field(default=None)
    price: float = field(default=None)
    events: List[str] = field(default_factory=list)
    event_price: float | None = field(default=None)


@dataclass(kw_only=True)
class SearchResultResponseDto(DtoIfs):
    categories: List[SearchResultCategoryResponseDto] = field(default_factory=list)
    events: List[SearchResultEventResponseDto] = field(default_factory=list)
    brands: List[SearchResultBrandResponseDto] = field(default_factory=list)
    sorts: List[SearchResultSortResponseDto] = field(default_factory=list)
    selected: SearchResultSelectedOptionResponseDto = field(
        default_factory=SearchResultSelectedOptionResponseDto
    )
    products: List[SearchResultProductResponseDto] = field(default_factory=list)
