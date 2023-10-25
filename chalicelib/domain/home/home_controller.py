from chalice import BadRequestError, Blueprint
from dependency_injector.wiring import Provide

from chalicelib.common.model.api import Api
from chalicelib.common.model.builder import ApiBuilder
from chalicelib.domain.home.home_service import HomeService
from chalicelib.interface.controller import Controller


class HomeController(Controller):
    api = Blueprint(__name__)
    service: HomeService = Provide["home_service"]

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
        data = HomeController.service.get_list(type=type)
        res = {
            type: data,
        }
        if type == "stores":
            res["search"] = None
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(res)
            .build()
        )
        return api
