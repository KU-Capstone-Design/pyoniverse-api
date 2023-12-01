from asyncio import AbstractEventLoop
from math import ceil
from typing import Set

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
    SearchResultResponseMetaDto,
)
from chalicelib.entity.product import ProductEntity
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
        # 1. query="" 이면 모든 상품을 가져온다. 검색 X
        if not request.query:
            filter_key = "status"
            filter_value = [1]
            # 필터를 API에서 수행함으로써 현재 DB에서 가져오는 데이터 수는 의미없다
            # total_size = self.__loop.run_until_complete(
            #         self.__product_service.get_length(
            #                 filter_key=filter_key,
            #                 filter_value=filter_value,
            #         )
            # )
        else:
            # 1. Search Service를 이용해 검색 시도
            filter_key = "id"
            filter_value = self.__loop.run_until_complete(
                self.__search_service.find_products(query=query)
            )
            # 필터를 API에서 수행함으로써 현재 DB에서 가져오는 데이터 수는 의미없다
            # total_size = len(filter_value)
        # total_page = ceil(total_size / request.page_size)

        # 2. 상품 가져오기
        if request.sort_key == "event_price":
            # best.price
            sort_key = "best.price"
        else:
            sort_key = request.sort_key
        # TODO : Command -> Builder 로 패턴 변경하기(복합 조건문을 사용할 필요가 있다)
        # action = self.__product_service.find_page(
        #     filter_key=filter_key,
        #     filter_value=filter_value,
        #     sort_key=sort_key,
        #     sort_direction=request.sort_direction,
        #     page=request.page,
        #     page_size=request.page_size,
        # )
        # 전체 데이터를 가져오기(lambda 내에서 pagination, category, brand, event filter를 적용한다.
        action = self.__product_service.find_in_sort_by(
            filter_key=filter_key,
            filter_value=filter_value,
            sort_key=sort_key,
            direction=request.sort_direction,
        )
        try:
            product_entities = self.__loop.run_until_complete(action)
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

        brand_map = {
            cb.id: SearchResultBrandResponseDto(id=cb.id, name=cb.name, image=cb.image)
            for cb in constant_brands
        }
        brands = {}
        for product in product_entities:
            brands.update({b.id: brand_map[b.id] for b in product.brands})
        brands = list(brands.values())

        # 8. 반횐될 products 생성
        # category, brand, event filter 적용하기
        category_filter: Set[int] = set(
            request.categories or [c.id for c in categories]
        )
        brand_filter: Set[int] = set(request.brands or [b.id for b in brands])
        event_filter: Set[int] = set(request.events or [e.id for e in events])

        products = []
        for product in product_entities:
            # 1. category filter 적용
            product: ProductEntity = product
            if product.category not in category_filter:
                continue
            # 2. brand filter 적용
            is_ok = False
            for b in product.brands:
                if b.id in brand_filter:
                    is_ok = True
                    break
            if not is_ok:
                continue
            # 3. event filter 적용
            is_ok = False
            for b in product.brands:
                if event_filter.intersection(b.events):
                    is_ok = True
                    break
            if not is_ok:
                continue

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

        # pagination 수행
        # 현재 페이지가 총 페이지보다 많다면 []를 반환하고, 현재 페이지를 마지막 페이지로 변경한다.
        total_size = len(products)
        total_page = ceil(total_size / request.page_size)
        current_page = min(request.page, total_page)
        products = products[
            (current_page - 1) * request.page_size : current_page * request.page_size
        ]

        meta = SearchResultResponseMetaDto(
            current_page=current_page,
            total_page=total_page,
            current_size=len(products),
            total_size=total_size,
            page_size=request.page_size,
            sort_key=request.sort_key,
            sort_direction=request.sort_direction,
            categories=list(category_filter),
            brands=list(brand_filter),
            events=list(event_filter),
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
