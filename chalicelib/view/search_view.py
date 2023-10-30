from chalice import Blueprint
from dependency_injector.wiring import Provide

from chalicelib.business.interface.business import SearchBusinessIfs
from chalicelib.view.model.api import Api
from chalicelib.view.model.builder import ApiBuilder


class SearchView:
    api = Blueprint(__name__)
    business: SearchBusinessIfs = Provide["search_business"]

    @staticmethod
    @api.route("/search", methods=["GET", "HEAD"], cors=True)
    def index() -> Api:
        response = SearchView.business.get_index()
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api
