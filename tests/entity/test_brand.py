from dataclasses import asdict, fields

import pytest

from chalicelib.entity.brand import BrandEntity


@pytest.fixture
def brand_entity():
    return {
        "_id": {"$oid": "652f808cd27bfe47fd517cbe"},
        "id": 2,
        "slug": "cu",
        "name": "CU",
        "meta": {"description": "CU Store Main Page"},
        "description": "CU Store Description",
        "events": [
            {
                "brand": "CU",
                "image": "https://dev-image.pyoniverse.kr/dev/events/ea282a0e78cbea565888fd205af5324b5552a088.webp",
                "name": "알뜰택배 무제한 할인 이벤트",
                "id": 5,
                "image_alt": "알뜰택배 무제한 할인 이벤트 thumbnail",
                "start_at": "2023-08-31",
                "end_at": "2023-10-30",
                "good_count": 0,
                "view_count": 0,
            },
            {
                "brand": "CU",
                "image": "https://dev-image.pyoniverse.kr/dev/events/ea282a0e78cbea565888fd205af5324b5552a088.webp",
                "name": "알뜰택배 무제한 할인 이벤트",
                "id": 5,
                "image_alt": "알뜰택배 무제한 할인 이벤트 thumbnail",
                "start_at": "2023-08-31",
                "end_at": "2023-10-30",
                "good_count": 0,
                "view_count": 0,
            },
            {
                "brand": "CU",
                "image": "https://dev-image.pyoniverse.kr/dev/events/ea282a0e78cbea565888fd205af5324b5552a088.webp",
                "name": "알뜰택배 무제한 할인 이벤트",
                "id": 5,
                "image_alt": "알뜰택배 무제한 할인 이벤트 thumbnail",
                "start_at": "2023-08-31",
                "end_at": "2023-10-30",
                "good_count": 0,
                "view_count": 0,
            },
        ],
        "products": [
            {
                "id": 8,
                "image": "https://dev-image.pyoniverse.kr/products/3d81e45d0299c61d6993260d521755579b662775.webp",
                "image_alt": "2021)냉장고바지 thumbnail",
                "name": "2021)냉장고바지",
                "good_count": 0,
                "view_count": 0,
                "price": 11500,
                "events": ["NEW"],
                "event_price": None,
            },
            {
                "id": 9,
                "image": "https://dev-image.pyoniverse.kr/products/ebc709bf74f400817cde4a787107837e7bbeb797.webp",
                "image_alt": "2021)목토시_검정색 thumbnail",
                "name": "2021)목토시_검정색",
                "good_count": 0,
                "view_count": 0,
                "price": 5500,
                "events": ["NEW"],
                "event_price": None,
            },
            {
                "id": 10,
                "image": "https://dev-image.pyoniverse.kr/products/387b31b88fe0e86c20d0a521de5140d951a61344.webp",
                "image_alt": "2021)목토시_프리미엄(검) thumbnail",
                "name": "2021)목토시_프리미엄(검)",
                "good_count": 0,
                "view_count": 0,
                "price": 7500,
                "events": ["NEW"],
                "event_price": None,
            },
        ],
        "image": "https://dev-image.pyoniverse.kr/brands/cu-logo.webp",
        "image_alt": "CU Logo image",
        "status": 1,
        "updated_at": {"$date": "2023-10-24T09:19:15.185Z"},
        "created_at": {"$date": "2023-10-24T05:17:00.031Z"},
    }


def test_brand_entity(brand_entity):
    # when
    brand = BrandEntity.from_dict(brand_entity)
    # then
    res = asdict(brand)
    for _field in fields(brand):
        assert res[_field.name] == brand_entity[_field.name]
