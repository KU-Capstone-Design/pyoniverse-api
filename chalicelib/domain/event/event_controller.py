from typing import Type

from chalice import Blueprint

from chalicelib.interfaces.controller import Controller
from chalicelib.interfaces.factories.service_factory import ServiceFactory
from chalicelib.interfaces.service import Service
from chalicelib.models.builder import ApiBuilder


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
        data = EventController.service.get_list(brand=brand_slug)
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
    def get_single(self, id: str):
        data = EventController.service.get_single(id=id)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(data)
            .build()
        )
        return api
