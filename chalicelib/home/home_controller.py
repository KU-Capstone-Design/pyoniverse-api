from typing import Type

from chalice import BadRequestError, Blueprint

from chalicelib.dtos.api import Api
from chalicelib.dtos.builder import ApiBuilder
from chalicelib.factories.service_factory import ServiceFactory
from chalicelib.interfaces.controller import Controller
from chalicelib.interfaces.service import Service


class HomeController(Controller):
    api = Blueprint(__name__)
    service: Type[Service] = ServiceFactory.create_service("home_service")

    @staticmethod
    @api.route("/home", methods=["GET", "HEAD"], cors=True)
    def index() -> Api:
        params = HomeController.api.current_request.query_params
        if not params:
            type = "stores"
        else:
            type = params.get("type")
            if type not in ["events", "products"]:
                raise BadRequestError(
                    f"Invalid type: {type}. Valid types are: events, products"
                )
        stores = HomeController.service.get_list(type=type)
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
