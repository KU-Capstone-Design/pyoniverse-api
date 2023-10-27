from chalice import Blueprint
from dependency_injector.wiring import Provide

from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.interface.business import BrandBusinessIfs
from chalicelib.common.model.api import Api
from chalicelib.common.model.builder import ApiBuilder
from chalicelib.interface.controller import Controller


class BrandController(Controller):
    api = Blueprint(__name__)
    business: BrandBusinessIfs = Provide["brand_business"]

    @staticmethod
    @api.route("/brand/{slug}", methods=["GET", "HEAD"], cors=True)
    def index(slug: str) -> Api:
        request = BrandRequestDto(slug=slug)
        response = BrandController.business.get_detail_page(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api
