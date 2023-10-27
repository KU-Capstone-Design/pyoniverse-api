from chalice import BadRequestError, Blueprint
from dependency_injector.wiring import Provide

from chalicelib.business.home.dto.request import HomeRequestDto
from chalicelib.business.interface.business import HomeBusinessIfs
from chalicelib.common.model.api import Api
from chalicelib.common.model.builder import ApiBuilder


class HomeView:
    api = Blueprint(__name__)
    business: HomeBusinessIfs = Provide["home_business"]

    @staticmethod
    @api.route("/home", methods=["GET", "HEAD"], cors=True)
    def index() -> Api:
        params = HomeView.api.current_request.query_params
        if not params:
            _type = "stores"
        else:
            _type = params.get("type")
            if _type not in ["events", "products", "stores"]:
                raise BadRequestError(
                    f"Invalid type: {_type}. Valid types are: events, products, stores"
                )
        request = HomeRequestDto(type=_type)
        response = HomeView.business.get_list(request)
        # res = {
        #     _type: data,
        # }
        # if _type == "stores":
        #     res["search"] = None
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api
