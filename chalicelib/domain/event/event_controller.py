from typing import Type

from chalice import Blueprint

from chalicelib.interface.controller import Controller
from chalicelib.interface.factories.service_factory import ServiceFactory
from chalicelib.interface.service import Service
from chalicelib.model.builder import ApiBuilder


class EventController(Controller):
    api = Blueprint(__name__)
    service: Type[Service] = ServiceFactory.create_service("event_service")

    @staticmethod
    @api.route("/events", methods=["GET", "HEAD"], cors=True)
    def get_default_list():
        # /events/cu 로 라우팅
        return EventController.get_list("cu")

    @staticmethod
    @api.route("/events/{brand_slug}", methods=["GET", "HEAD"], cors=True)
    def get_list(brand_slug: str):
        data = EventController.service.get_single(_type="list", id=brand_slug)
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
    def get_detail(id: str):
        data = EventController.service.get_single(_type="detail", id=id)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(data)
            .build()
        )
        return api
