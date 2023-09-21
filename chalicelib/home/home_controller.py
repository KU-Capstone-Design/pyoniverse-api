from typing import Type

from chalice import Blueprint

from chalicelib.dtos.api import Api
from chalicelib.dtos.builder import ApiBuilder
from chalicelib.factories.service_factory import ServiceFactory
from chalicelib.interfaces.controller import Controller
from chalicelib.interfaces.service import Service


class HomeController(Controller):
    api = Blueprint(__name__)
    service: Type[Service] = ServiceFactory.create_service("home_service")

    @staticmethod
    @api.route("/", methods=["GET", "HEAD"], cors=True)
    def index() -> Api:
        stores = HomeController.service.get_list(type="store")
        res = {
            "stores": stores,
            "search": None,
        }
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(res)
            .build()
        )
        return api
