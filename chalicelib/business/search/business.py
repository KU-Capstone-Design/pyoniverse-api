from asyncio import AbstractEventLoop

from chalice import NotFoundError

from chalicelib.business.interface.business import SearchBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    ProductServiceIfs,
)
from chalicelib.business.search.dto.request import SearchResultRequestDto
from chalicelib.business.search.dto.response import (
    SearchHomeResponseDto,
    SearchResultBrandResponseDto,
    SearchResultCategoryResponseDto,
    SearchResultEventResponseDto,
    SearchResultProductResponseDto,
    SearchResultResponseDto,
    SearchResultSelectedOptionResponseDto,
    SearchResultSortResponseDto,
)


class AsyncSearchBusiness(SearchBusinessIfs):
    def __init__(
        self,
        constant_brand_service: ConstantBrandServiceIfs,
        product_service: ProductServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__constant_brand_service = constant_brand_service
        self.__product_service = product_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__constant_brand_service, ConstantBrandServiceIfs)
        assert isinstance(self.__product_service, ProductServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_index(self) -> SearchHomeResponseDto:
        # TODO : DB Sync
        result = SearchHomeResponseDto(histories=[])
        return result

    def get_result(self, request: SearchResultRequestDto) -> SearchResultResponseDto:
        # TODO : DB Sync
        request.queries = [q.replace("%20", " ").strip() for q in request.queries]

        response = SearchResultResponseDto(
            categories=[
                SearchResultCategoryResponseDto(**{"id": None, "name": "전체"}),
                SearchResultCategoryResponseDto(**{"id": 1, "name": "과자류"}),
            ],
            events=[
                SearchResultEventResponseDto(**{"id": None, "name": "전체"}),
                SearchResultEventResponseDto(**{"id": 1, "name": "1+1"}),
            ],
            brands=[
                SearchResultBrandResponseDto(**{"id": None, "name": "전체"}),
                SearchResultBrandResponseDto(
                    **{
                        "id": 1,
                        "name": "GS25",
                        "image": "https://dev-image.pyoniverse.kr/"
                        "brands/gs25-logo.webp",
                    }
                ),
            ],
            sorts=[
                SearchResultSortResponseDto(**{"id": 1, "name": "Good Count"}),
                SearchResultSortResponseDto(**{"id": 2, "name": "View Count"}),
            ],
            selected=SearchResultSelectedOptionResponseDto(
                **{
                    "category": 1,
                    "event": 1,
                    "brand": 1,
                    "sort": 1,
                    "direction": "asc",
                }
            ),
            products=[
                SearchResultProductResponseDto(
                    **{
                        "id": 1,
                        "name": "test-product-one",
                        "image": "https://dev-image.pyoniverse.kr/products/"
                        "ae5a223ab345c744c7179d3689adb6eb6eabc1a9.webp",
                        "image_alt": "test-product-image-alt",
                        "price": 1000,
                        "events": ["NEW", "1+1"],
                        "event_price": None,
                    }
                ),
                SearchResultProductResponseDto(
                    **{
                        "id": 2,
                        "name": "test-product-two",
                        "image": "https://dev-image.pyoniverse.kr/products/"
                        "79cd70e8235b951d16f8701e9f5629242ed8fca2.webp",
                        "image_alt": "test-product-image-alt",
                        "price": 1000,
                        "events": ["NEW", "SALE"],
                        "event_price": 900,
                    }
                ),
            ],
        )

        if not response.products:
            raise NotFoundError(f"products not in {request} search")
        return response
