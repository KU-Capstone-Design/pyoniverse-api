from asyncio import AbstractEventLoop, gather
from math import ceil
from typing import List

from chalice import NotFoundError

from chalicelib.business.interface.business import SearchBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    ProductServiceIfs,
    SearchServiceIfs,
)
from chalicelib.business.model.enum import OperatorEnum
from chalicelib.business.search.dto.request import SearchResultRequestDto
from chalicelib.business.search.dto.response import (
    SearchHomeResponseDto,
    SearchResultBrandResponseDto,
    SearchResultCategoryResponseDto,
    SearchResultEventResponseDto,
    SearchResultProductResponseDto,
    SearchResultResponseDto,
    SearchResultResponseMetaDto,
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
        if request.sort_key == "event_price":
            # best.price
            sort_key = "best.price"
        else:
            sort_key = request.sort_key
        queries = []
        if request.categories:
            queries.append([OperatorEnum.IN, "category", request.categories])
        if request.brands:
            queries.append([OperatorEnum.IN, "brands.id", request.brands])
        if request.events:
            queries.append(
                [
                    OperatorEnum.ELEM_MATCH,
                    OperatorEnum.IN,
                    "brands.events",
                    request.events,
                ]
            )

        if not request.query:
            # 1. query="" 이면 모든 상품을 가져온다. 검색 X
            search_op = [OperatorEnum.EQUAL, "status", 1]
            queries.append(search_op)
        else:
            # 1. Search Service를 이용해 검색 시도
            searched_ids = self.__loop.run_until_complete(
                self.__search_service.find_products(query=query)
            )
            search_op = [OperatorEnum.IN, "id", searched_ids]
            # 필터를 API에서 수행함으로써 현재 DB에서 가져오는 데이터 수는 의미없다
            queries.append(search_op)
        # Category, Brand, Event 가져오기
        category_action = self.__product_service.distinct("category", [search_op])
        brand_action = self.__product_service.distinct("brands.id", [search_op])
        event_action = self.__product_service.distinct("brands.events", [search_op])
        # Query 수행
        search_action = self.__product_service.search(
            queries=queries,
            sort_key=sort_key,
            direction=request.sort_direction,
            page=request.page,
            page_size=request.page_size,
        )
        size_action = self.__product_service.get_length(queries=queries)
        try:
            (
                total_size,
                product_entities,
                total_categories,
                total_brands,
                total_events,
            ) = self.__loop.run_until_complete(
                gather(
                    size_action,
                    search_action,
                    category_action,
                    brand_action,
                    event_action,
                )
            )
            total_page = ceil(total_size / request.page_size)
        except NotFoundError:
            product_entities = []
            total_size = 0
            total_page = 0
            total_categories = set()
            total_brands = set()
            total_events = set()
        if request.page > total_page:
            product_entities = []

        constant_brands = self.__loop.run_until_complete(
            self.__constant_brand_service.find_all()
        )
        # 3. category 정보 가져오기
        categories: List[SearchResultCategoryResponseDto] = [
            SearchResultCategoryResponseDto(
                id=int(c),
                name=ConstantConverter.convert_category_id(int(c))["name"],
            )
            for c in total_categories
            if c is not None
        ]
        # 4. event 정보 가져오기
        events: List[SearchResultEventResponseDto] = [
            SearchResultEventResponseDto(
                id=int(e), name=ConstantConverter.convert_event_id(int(e))["name"]
            )
            for e in total_events
            if e is not None
        ]

        brand_map = {
            cb.id: SearchResultBrandResponseDto(id=cb.id, name=cb.name, image=cb.image)
            for cb in constant_brands
        }
        brands: List[SearchResultBrandResponseDto] = [
            brand_map[int(b)] for b in total_brands if b is not None
        ]

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
                category=int(product.category) if product.category else None,
                brands=list(map(lambda x: x.id, product.brands)),
            )
            products.append(res_product)

        meta = SearchResultResponseMetaDto(
            current_page=request.page,
            total_page=total_page,
            current_size=len(products),
            total_size=total_size,
            page_size=request.page_size,
            sort_key=request.sort_key,
            sort_direction=request.sort_direction,
            categories=sorted([c.id for c in categories]),
            brands=sorted([b.id for b in brands]),
            events=sorted([e.id for e in events]),
        )
        response = SearchResultResponseDto(
            categories=sorted(categories, key=lambda x: x.id),
            events=sorted(events, key=lambda x: x.id),
            brands=sorted(brands, key=lambda x: x.id),
            products=products,
            products_count=len(products),
            meta=meta,
        )
        return response
