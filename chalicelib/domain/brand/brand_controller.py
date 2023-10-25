from typing import Type

from chalice import Blueprint

from chalicelib.model.api import Api
from chalicelib.model.builder import ApiBuilder
from chalicelib.interface.factories.service_factory import ServiceFactory
from chalicelib.interface.controller import Controller
from chalicelib.interface.service import Service


class BrandController(Controller):
    api = Blueprint(__name__)
    service: Type[Service] = ServiceFactory.create_service("brand_service")

    @staticmethod
    @api.route("/brand/{slug}", methods=["GET", "HEAD"], cors=True)
    def index(slug: str) -> Api:
        data = BrandController.service.get_single(slug=slug)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(data)
            .build()
        )
        return api
