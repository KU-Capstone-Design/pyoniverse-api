from asyncio import AbstractEventLoop
from typing import List

from chalice import NotFoundError

from chalicelib.business.interface.business import SearchBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    ProductServiceIfs,
    SearchServiceIfs,
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
from chalicelib.entity.util import ConstantConverter


class AsyncSearchBusiness(SearchBusinessIfs):
    def __init__(
        self,
        search_service: SearchServiceIfs,
        constant_brand_service: ConstantBrandServiceIfs,
        product_service: ProductServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__search_service = search_service
        self.__constant_brand_service = constant_brand_service
        self.__product_service = product_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__search_service, SearchServiceIfs)
        assert isinstance(self.__constant_brand_service, ConstantBrandServiceIfs)
        assert isinstance(self.__product_service, ProductServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_index(self) -> SearchHomeResponseDto:
        # 중복된 상품이 선택되는 경우를 고려해 2배 더 많은 8개를 선택함
        random_products = self.__loop.run_until_complete(
            self.__product_service.random(chunk_size=8)
        )
        recommendations = list(set(p.name for p in random_products))[:4]
        result = SearchHomeResponseDto(histories=[], recommendations=recommendations)
        return result

    def get_result(self, request: SearchResultRequestDto) -> SearchResultResponseDto:
        query = request.query.replace("%20", " ")
        # 1. Search Service를 이용해 검색 시도
        search_results: List[int] = self.__loop.run_until_complete(
            self.__search_service.find_products(query=query)
        )
        # 2. id list에 맞는 상품 가져오기
        try:
            product_entities = self.__loop.run_until_complete(
                self.__product_service.find_in_sort_by(
                    filter_key="id",
                    filter_value=search_results,
                    sort_key="price",
                    direction="asc",
                )
            )
        except NotFoundError:
            product_entities = []
        constant_brands = self.__loop.run_until_complete(
            self.__constant_brand_service.find_all()
        )

        # 3. category 정보 가져오기
        categories = list(
            {
                p.category: SearchResultCategoryResponseDto(
                    id=int(p.category),
                    name=ConstantConverter.convert_category_id(p.category)["name"],
                )
                for p in product_entities
                if p.category is not None
            }.values()
        )
        categories.append(SearchResultCategoryResponseDto(id=None, name="전체"))
        # 4. event 정보 가져오기
        events = {}
        for product in product_entities:
            for brand in product.brands:
                events.update(
                    {
                        id_: SearchResultEventResponseDto(
                            id=id_, name=ConstantConverter.convert_event_id(id_)["name"]
                        )
                        for id_ in brand.events
                    }
                )
        events = list(events.values())
        events.append(SearchResultEventResponseDto(id=None, name="전체"))
        # 5. brand 정보 가져오기
        # constant_brands = self.__loop.run_until_complete(
        #         self.__constant_brand_service.find_all()
        # )
        brand_map = {
            cb.id: SearchResultBrandResponseDto(id=cb.id, name=cb.name, image=cb.image)
            for cb in constant_brands
        }
        brands = {}
        for product in product_entities:
            brands.update({b.id: brand_map[b.id] for b in product.brands})
        brands = list(brands.values())
        brands.append(SearchResultBrandResponseDto(id=None, name="전체", image=None))

        # 6. sort # TODO : 아직 협의되지 않음 - price 순서로 정렬
        sorts = [
            SearchResultSortResponseDto(id=1, name="Good Count"),
            SearchResultSortResponseDto(id=2, name="View Count"),
            SearchResultSortResponseDto(id=3, name="price"),
        ]
        # 7. 필터 적용 # TODO :
        selected = SearchResultSelectedOptionResponseDto(
            category=None,
            event=None,
            brand=None,
            sort=3,
            direction="asc",
        )
        # 8. 반횐될 products 생성
        products = []
        for product in product_entities:
            if product.price == product.best.price:
                event_price = None
            else:
                event_price = product.best.price
            res_product = SearchResultProductResponseDto(
                id=product.id,
                name=product.name,
                image=product.image,
                image_alt=f"{product.name}",
                price=product.price,
                events=[
                    ConstantConverter.convert_event_id(id_)["name"]
                    for id_ in product.best.events
                ],
                event_price=event_price,
            )
            products.append(res_product)
        # 9. 정렬 기준에 맞춰 정렬 - 현재 price asc
        products = sorted(products, key=lambda x: x.price)

        response = SearchResultResponseDto(
            categories=categories,
            events=events,
            brands=brands,
            sorts=sorts,
            selected=selected,
            products=products,
        )
        return response
