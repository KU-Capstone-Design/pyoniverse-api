from chalice import Blueprint
from dependency_injector.wiring import Provide

from chalicelib.business.event.dto.request import EventRequestDto
from chalicelib.business.interface.business import EventBusinessIfs
from chalicelib.view.model.builder import ApiBuilder


class EventView:
    api = Blueprint(__name__)
    business: EventBusinessIfs = Provide["event_business"]

    @staticmethod
    @api.route("/events", methods=["GET", "HEAD"], cors=True)
    def get_default_list():
        # /events/cu 로 라우팅
        return EventView.get_list("cu")

    @staticmethod
    @api.route("/events/{brand_slug}", methods=["GET", "HEAD"], cors=True)
    def get_list(brand_slug: str):
        request = EventRequestDto(brand_slug=brand_slug)
        data = EventView.business.get_list(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(data)
            .build()
        )
        return api

    @staticmethod
    @api.route("/event/{id}", methods=["GET", "HEAD"], cors=True)
    def get_detail(id: int):
        request = EventRequestDto(id=int(id))
        data = EventView.business.get_detail(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(data)
            .build()
        )
        return api
