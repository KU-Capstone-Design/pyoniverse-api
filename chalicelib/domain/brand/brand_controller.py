from chalice import Blueprint
from dependency_injector.wiring import Provide

from chalicelib.common.model.api import Api
from chalicelib.common.model.builder import ApiBuilder
from chalicelib.domain.brand.brand_service import BrandService
from chalicelib.interface.controller import Controller


class BrandController(Controller):
    api = Blueprint(__name__)
    service: BrandService = Provide["brand_service"]

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
