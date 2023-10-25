import json

import pytest

from chalicelib.common.model import ApiBuilder
from chalicelib.common.model import JsonSerializer
from chalicelib.entity.product import ProductEntity


@pytest.fixture
def product_entity():
    return {
        "crawled_infos": [
            {
                "spider": "gs25web",
                "id": "GD_2700038840545_002",
                "url": "http://gs25.gsretail.com/products/youus-freshfoodDetail-"
                "search?CSRFToken=fb1fe0ed-cf6b-42ed-9ec2-e8c7955ab41c",
                "brand": 1,
            }
        ],
        "brands": [
            {
                "id": 1,
                "price": {"value": 5200, "currency": 1, "discounted_value": None},
                "event": [4],
            }
        ],
        "category": 6,
        "description": None,
        "image": "s3://pyoniverse-image/product/00646d43e6ac14744acb4aa49c1fa3947a5c4d09.webp",
        "name": "11가지찬많은도시락1편",
        "recommendation": [{"product": [], "event": []}],
        "status": 1,
        "id": 0,
    }


def test_product_entity(product_entity):
    entity = ProductEntity.from_dict(product_entity)

    assert entity.id == product_entity["id"]
    assert entity.name == product_entity["name"]
    assert entity.category == product_entity["category"]
    assert entity.image == product_entity["image"]
    assert entity.description == product_entity["description"]
    for entity_brand, brand in zip(entity.brands, product_entity["brands"]):
        assert entity_brand.id == brand["id"]
        assert entity_brand.price.value == brand["price"]["value"]
        assert entity_brand.price.currency == brand["price"]["currency"]
        assert entity_brand.price.discounted_value == brand["price"]["discounted_value"]
        assert entity_brand.events == brand["event"]


def test_serializer():
    mock = ApiBuilder().with_status_code("200 OK").with_status_message("OK").build()
    assert JsonSerializer.serialize(mock) == json.dumps(
        {
            "status_code": "200 OK",
            "status_message": "OK",
            "data": None,
            "errors": None,
            "pagination": None,
        },
        ensure_ascii=False,
    )
