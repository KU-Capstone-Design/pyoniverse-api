from typing import Dict, Type

from chalicelib.entity.base import BaseEntity
from chalicelib.entity.brand import BrandEntity
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity


ENTITY_MAP: Dict[str, Dict[str, Type[BaseEntity]]] = {
    "constant": {
        "brands": ConstantBrandEntity,
    },
    "service": {
        "brands": BrandEntity,
        "events": EventEntity,
        "products": ProductEntity,
    },
}
