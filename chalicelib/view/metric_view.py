from chalice import BadRequestError, Blueprint
from dependency_injector.wiring import Provide

from chalicelib.business.interface.business import MetricBusinessIfs
from chalicelib.business.metric.model.request import MetricRequestDto
from chalicelib.view.model.api import Api
from chalicelib.view.model.builder import ApiBuilder


class MetricView:
    api = Blueprint(__name__)
    business: MetricBusinessIfs = Provide["metric_business"]

    @staticmethod
    @api.route("/metric/good", methods=["GET", "HEAD"], cors=True)
    def get_good_count() -> Api:
        params = MetricView.api.current_request.query_params
        request = MetricRequestDto(
            id=params.get("id"),
            domain=params.get("domain"),
        )
        try:
            request.id = int(request.id)
        except ValueError:
            raise BadRequestError(f"{request.id} should be int type")

        if not request.domain:
            raise BadRequestError(f"{request.domain} should be in ['product', 'event']")

        response = MetricView.business.get_good_count(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api

    @staticmethod
    @api.route("/metric/view", methods=["GET", "HEAD"], cors=True)
    def get_view_count() -> Api:
        params = MetricView.api.current_request.query_params
        request = MetricRequestDto(
            id=params.get("id"),
            domain=params.get("domain"),
        )
        try:
            request.id = int(request.id)
        except ValueError:
            raise BadRequestError(f"{request.id} should be int type")

        if not request.domain:
            raise BadRequestError(f"{request.domain} should be in ['product', 'event']")

        response = MetricView.business.get_view_count(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api

    @staticmethod
    @api.route("/metric/good", methods=["PATCH"], cors=True)
    def update_good_count() -> Api:
        body: dict = MetricView.api.current_request.json_body
        request = MetricRequestDto(
            id=body.get("id"),
            domain=body.get("domain"),
            value=body.get("value"),
        )
        try:
            request.id = int(request.id)
            request.value = int(request.value)
        except ValueError:
            raise BadRequestError(
                f"{request.id} and {request.value} should be int type"
            )

        if not request.domain:
            raise BadRequestError(f"{request.domain} should be in ['product', 'event']")

        response = MetricView.business.update_good_count(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api

    @staticmethod
    @api.route("/metric/view", methods=["PATCH"], cors=True)
    def update_view_count() -> Api:
        body: dict = MetricView.api.current_request.json_body
        request = MetricRequestDto(
            id=body.get("id"),
            domain=body.get("domain"),
            value=body.get("value"),
        )
        try:
            request.id = int(request.id)
            request.value = int(request.value)
        except ValueError:
            raise BadRequestError(
                f"{request.id} and {request.value} should be int type"
            )

        if not request.domain:
            raise BadRequestError(f"{request.domain} should be in ['product', 'event']")

        response = MetricView.business.update_view_count(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api
