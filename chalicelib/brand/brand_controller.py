from typing import Type

from chalice import Blueprint

from chalicelib.dtos.api import Api
from chalicelib.dtos.builder import ApiBuilder
from chalicelib.factories.service_factory import ServiceFactory
from chalicelib.interfaces.controller import Controller
from chalicelib.interfaces.service import Service


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
