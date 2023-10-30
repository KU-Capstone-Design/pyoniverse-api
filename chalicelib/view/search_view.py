from chalice import BadRequestError, Blueprint
from chalice.app import MultiDict
from dependency_injector.wiring import Provide

from chalicelib.business.interface.business import SearchBusinessIfs
from chalicelib.business.search.dto.request import SearchResultRequestDto
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

    @staticmethod
    @api.route("/search/result", methods=["GET", "HEAD"], cors=True)
    def index() -> Api:
        params: MultiDict = SearchView.api.current_request.query_params
        if not params or not params.getlist("query"):
            raise BadRequestError("Empty Query")
        request = SearchResultRequestDto(
            queries=params.getlist("query"),
            sort=params.get("sort"),
            direction=params.get("direction"),
            category=params.get("category"),
            event=params.get("event"),
            brand=params.get("brand"),
        )

        response = SearchView.business.get_result(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api
