from dataclasses import asdict, fields

import pytest

from chalicelib.entity.event import EventEntity


@pytest.fixture
def event_entity():
    return {
        "_id": {"$oid": "65331eb477ce31f96a750414"},
        "crawled_infos": [
            {
                "spider": "sevenelevenweb_event",
                "id": "1021",
                "url": "https://m.7-eleven.co.kr:444/product/eventView.asp",
                "brand": 3,
            }
        ],
        "brand": 3,
        "description": None,
        "end_at": 1698710400,
        "image": {
            "thumb": "https://dev-image.pyoniverse.kr/events/de4e163e2c6068cb8aa533b5950ab1f6bbbe522e.webp",
            "others": [],
        },
        "name": "신한 lplay결제시 핫 전종 반값",
        "start_at": 1696118400,
        "status": 1,
        "created_at": {"$date": "2023-10-21T00:43:33.096Z"},
        "good_count": {"$numberLong": "0"},
        "id": 1,
        "updated_at": {"$date": "2023-10-24T09:13:40.112Z"},
        "view_count": {"$numberLong": "0"},
    }


def test_event_entity(event_entity):
    # when
    event = EventEntity.from_dict(event_entity)
    # then
    res = asdict(event)
    for _field in fields(event):
        assert res[_field.name] == event_entity[_field.name]
