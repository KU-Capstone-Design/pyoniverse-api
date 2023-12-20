import asyncio
from asyncio import AbstractEventLoop, gather
from datetime import datetime
from typing import Sequence

from chalice import BadRequestError

from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.brand.dto.response import (
    BrandEventResponseDto,
    BrandMetaResponseDto,
    BrandProductResponseDto,
    BrandResponseDto,
)
from chalicelib.business.interface.business import BrandBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    EventServiceIfs,
    ProductServiceIfs,
)
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductBrandEntity, ProductEntity
from chalicelib.entity.util import ConstantConverter


class AsyncBrandBusiness(BrandBusinessIfs):
    def __init__(
        self,
        constant_brand_service: ConstantBrandServiceIfs,
        product_service: ProductServiceIfs,
        event_service: EventServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__constant_brand_service = constant_brand_service
        self.__product_service = product_service
        self.__event_service = event_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__constant_brand_service, ConstantBrandServiceIfs)
        assert isinstance(self.__product_service, ProductServiceIfs)
        assert isinstance(self.__event_service, EventServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_detail_page(self, request: BrandRequestDto) -> BrandResponseDto:
        if not isinstance(request, BrandRequestDto):
            raise BadRequestError(f"{request} should be BrandRequestDto type")
        if not isinstance(request.slug, str):
            raise BadRequestError(f"{request.slug} should be str type")
        # 1. constant 정보 불러오기
        constant_brand: ConstantBrandEntity = ConstantBrandEntity(slug=request.slug)
        constant_brand = self.__loop.run_until_complete(
            self.__constant_brand_service.find_by_slug(constant_brand)
        )
        # 2. product 정보 불러오기 - good_count 순서
        products: Sequence[ProductEntity] = self.__product_service.find_chunk_by(
            filter_key="brands.id",
            filter_value=constant_brand.id,
            sort_key="good_count",
            direction="desc",
            chunk_size=3,
        )
        # 3. event 정보 불러오기
        events: Sequence[EventEntity] = self.__event_service.find_chunk_by(
            filter_key="brand",
            filter_value=constant_brand.id,
            sort_key="good_count",
            direction="desc",
            chunk_size=3,
        )
        # await
        products, events = self.__loop.run_until_complete(gather(products, events))
        # make
        product_responses = []
        for product in products:
            cur_brand_info: ProductBrandEntity = next(
                filter(lambda x: x.id == constant_brand.id, product.brands)
            )
            # product_events = [
            #     ConstantConverter.convert_event_id(e)["name"]
            #     for e in cur_brand_info.events
            # ]
            product_events = sorted(cur_brand_info.events)
            event_price = cur_brand_info.price.discounted_value
            tmp = BrandProductResponseDto(
                id=product.id,
                image=product.image,
                image_alt=f"{product.name} image",
                name=product.name,
                good_count=product.good_count,
                view_count=product.view_count,
                price=product.price,
                events=product_events,
                event_price=event_price,
            )
            product_responses.append(tmp)

        event_responses = []
        for event in events:
            tmp = BrandEventResponseDto(
                brand=constant_brand.slug,
                image=event.image.thumb,
                name=event.name,
                id=event.id,
                image_alt=f"{event.name} image",
                start_at=datetime.fromtimestamp(event.start_at).strftime("%Y-%m-%d"),
                end_at=datetime.fromtimestamp(event.end_at).strftime("%Y-%m-%d"),
                good_count=event.good_count,
                view_count=event.view_count,
            )
            event_responses.append(tmp)

        result = BrandResponseDto(
            id=constant_brand.id,
            slug=constant_brand.slug,
            name=constant_brand.name,
            image=constant_brand.image,
            image_alt=f"{constant_brand.name} image",
            description=f"{constant_brand.name} Page",
            meta=BrandMetaResponseDto(description=f"{constant_brand.name} Page"),
            products=product_responses,
            events=event_responses,
        )
        return result
