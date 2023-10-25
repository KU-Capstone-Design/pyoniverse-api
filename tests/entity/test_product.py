from dataclasses import asdict, fields

import pytest

from chalicelib.entity.product import ProductEntity


@pytest.fixture
def product_entity():
    return {
        "_id": {"$oid": "65331ec677ce31f96a751003"},
        "crawled_infos": [
            {
                "spider": "gs25web",
                "id": "GD_2700038851725_002",
                "url": "http://gs25.gsretail.com/products/youus-freshfoodDetail-search?"
                "CSRFToken=8f31834d-d41f-4bf5-a30c-5c5a34c6f4ea",
                "brand": 1,
            }
        ],
        "best": {"price": 5500, "brand": 1, "events": [4]},
        "brands": [
            {
                "id": 1,
                "price": {"value": 5500, "currency": 1, "discounted_value": None},
                "events": [4],
            }
        ],
        "category": 6,
        "description": None,
        "image": "https://dev-image.pyoniverse.kr/products/ae5a223ab345c744c7179d3689adb6eb6eabc1a9.webp",
        "name": "11가지찬많은도시락1편",
        "price": 5500,
        "recommendation": {"products": [], "events": []},
        "status": 1,
        "created_at": {"$date": "2023-10-21T01:57:55.935Z"},
        "good_count": 0,
        "updated_at": {"$date": "2023-10-24T09:17:27.813Z"},
        "view_count": 0,
        "id": 1,
        "histories": [],
    }


def test_product_entity(product_entity):
    # when
    product = ProductEntity.from_dict(product_entity)
    # then
    res = asdict(product)
    for _field in fields(product):
        assert res[_field.name] == product_entity[_field.name]
