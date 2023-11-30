from chalicelib.business.event.business import AsyncEventBusiness
from chalicelib.business.event.dto.request import EventRequestDto
from chalicelib.business.event.dto.response import (
    EventDetailResponseDto,
    EventsResponseDto,
)
from chalicelib.converter.event import EventConverter


def test_event_business(constant_brand_service, event_service, event_loop):
    # given
    business = AsyncEventBusiness(
        constant_brand_service=constant_brand_service,
        event_service=event_service,
        converter=EventConverter(),
        loop=event_loop,
    )
    # when
    event_list_response = business.get_list(EventRequestDto(brand_slug="cu"))
    event_detail_response = business.get_detail(EventRequestDto(id=1))
    # then
    assert isinstance(event_list_response, EventsResponseDto)
    assert isinstance(event_detail_response, EventDetailResponseDto)
