from dataclasses import dataclass, field
from typing import List

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class ProductBrandHistoryResponseDto:
    date: str = field(default=None)
    events: List[str] = field(default_factory=list)
    price: float = field(default=None)
    event_price: float | None = field(default=None)


@dataclass(kw_only=True)
class ProductHistoriesSummaryPriceResponseDto:
    brand: str = field(default=None)
    value: float = field(default=None)
    date: str = field(default=None)


@dataclass(kw_only=True)
class ProductHistoriesSummaryResponseDto:
    lowest_price: ProductHistoriesSummaryPriceResponseDto = field(
        default_factory=ProductHistoriesSummaryPriceResponseDto
    )
    highest_price: ProductHistoriesSummaryPriceResponseDto = field(
        default_factory=ProductHistoriesSummaryPriceResponseDto
    )


@dataclass(kw_only=True)
class ProductBrandResponseDto:
    id: int = field(default=None)
    name: str = field(default=None)
    image: str = field(default=None)
    events: List[str] = field(default_factory=list)
    price: float = field(default=None)
    event_price: float | None = field(default=None)  # 가격과 행사 가격이 동일하면 None으로 처리
    histories: List[ProductBrandHistoryResponseDto] = field(default_factory=list)
    histories_summary: ProductHistoriesSummaryResponseDto = field(
        default_factory=ProductHistoriesSummaryResponseDto
    )


@dataclass(kw_only=True)
class ProductResponseDto(DtoIfs):
    id: int = field(default=None)
    name: str = field(default=None)
    price: float = field(default=None)
    image: str = field(default=None)
    image_alt: str = field(default=None)
    best_brand: int = field(default=None)
    brands: List[ProductBrandResponseDto] = field(default_factory=list)
    good_count: int = field(default=None)
    view_count: int = field(default=None)
