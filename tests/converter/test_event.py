from datetime import datetime

from chalicelib.business.event.dto.response import (
    EventDetailResponseDto,
    EventSimpleResponseDto,
)
from chalicelib.converter.event import EventConverter
from chalicelib.entity.event import EventEntity, EventImageEntity


def test_event_converter():
    # given
    converter = EventConverter()
    entity = EventEntity(
        brand=3,
        start_at=1696118400,
        end_at=1698710400,
        image=EventImageEntity(
            thumb="https://dev-image.pyoniverse.kr/events/de4e163e2c6068cb8aa533b5950ab1f6bbbe522e.webp"
        ),
        name="신한 lplay결제시 핫 전종 반값",
        status=1,
        good_count=0,
        view_count=0,
        id=1,
    )
    # when
    detail_response = converter.convert_to_dto(entity, EventDetailResponseDto)
    simple_response = converter.convert_to_dto(entity, EventSimpleResponseDto)
    # then
    try:
        datetime.strptime(detail_response.start_at, "%m/%d")
        datetime.strptime(detail_response.end_at, "%m/%d")
        datetime.strptime(simple_response.start_at, "%m/%d")
        datetime.strptime(simple_response.end_at, "%m/%d")
    except Exception as e:
        assert False
    else:
        assert True
