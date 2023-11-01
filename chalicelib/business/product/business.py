from asyncio import AbstractEventLoop, gather
from datetime import datetime
from typing import Dict, List

from chalicelib.business.interface.business import ProductBusinessIfs
from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.service import (
    ConstantBrandServiceIfs,
    ProductServiceIfs,
)
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.business.product.dto.response import (
    ProductBrandHistoryResponseDto,
    ProductBrandResponseDto,
    ProductResponseDto,
)
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.product import ProductBrandEntity, ProductEntity
from chalicelib.entity.util import ConstantConverter


class AsyncProductBusiness(ProductBusinessIfs):
    def __init__(
        self,
        product_service: ProductServiceIfs,
        constant_brand_service: ConstantBrandServiceIfs,
        converter: ConverterIfs,
        loop: AbstractEventLoop,
    ):
        self.__product_service = product_service
        self.__constant_brand_service = constant_brand_service
        self.__converter = converter
        self.__loop = loop

        assert isinstance(self.__product_service, ProductServiceIfs)
        assert isinstance(self.__constant_brand_service, ConstantBrandServiceIfs)
        assert isinstance(self.__converter, ConverterIfs)
        assert isinstance(self.__loop, AbstractEventLoop)

    def get_detail(self, request: ProductRequestDto) -> ProductResponseDto:
        entity = self.__converter.convert_to_entity(request)
        product_entity, constant_brand_entities = self.__loop.run_until_complete(
            gather(
                self.__product_service.find_one(entity),
                self.__constant_brand_service.find_all(),
            )
        )
        response: ProductResponseDto = self.__converter.convert_to_dto(product_entity)
        self._get_histories(constant_brand_entities, product_entity, response)
        return response

    def _get_histories(
        self,
        constant_brand_entities: List[ConstantBrandEntity],
        product_entity: ProductEntity,
        response,
    ):
        constant_brand_map: Dict[int, ConstantBrandEntity] = {
            e.id: e for e in constant_brand_entities
        }
        history_brand_checker = {
            h.date: {b.id for b in h.brands} for h in product_entity.histories
        }
        for brand in product_entity.brands:
            tmp = ProductBrandResponseDto(
                id=brand.id,
                name=constant_brand_map[brand.id].name,
                image=constant_brand_map[brand.id].image,
                events=list(
                    map(
                        lambda x: ConstantConverter.convert_event_id(x)["name"],
                        brand.events,
                    )
                ),
                price=brand.price.value,
                event_price=brand.price.discounted_value,
            )
            # add histories
            for history in product_entity.histories:
                if brand.id not in history_brand_checker[history.date]:
                    continue
                history_info: ProductBrandEntity = next(
                    filter(lambda x: x.id == brand.id, history.brands)
                )
                tmp.histories.append(
                    ProductBrandHistoryResponseDto(
                        date=history.date,
                        events=list(
                            map(
                                lambda x: ConstantConverter.convert_event_id(x)["name"],
                                history_info.events,
                            )
                        ),
                        price=history_info.price.value,
                        event_price=history_info.price.discounted_value,
                    )
                )
            # add self
            tmp.histories.append(
                ProductBrandHistoryResponseDto(
                    date=datetime.now().strftime("%Y-%m-%d"),
                    events=list(
                        map(
                            lambda x: ConstantConverter.convert_event_id(x)["name"],
                            brand.events,
                        )
                    ),
                    price=brand.price.value,
                    event_price=brand.price.discounted_value,
                )
            )
            # sort by date
            tmp.histories = sorted(
                tmp.histories, key=lambda x: x.date, reverse=True
            )  # Latest 순서
            response.brands.append(tmp)
