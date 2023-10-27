from chalice import Blueprint
from dependency_injector.wiring import Provide

from chalicelib.business.brand.dto.request import BrandRequestDto
from chalicelib.business.interface.business import BrandBusinessIfs
from chalicelib.view.model.api import Api
from chalicelib.view.model.builder import ApiBuilder


class BrandView:
    api = Blueprint(__name__)
    business: BrandBusinessIfs = Provide["brand_business"]

    @staticmethod
    @api.route("/brand/{slug}", methods=["GET", "HEAD"], cors=True)
    def index(slug: str) -> Api:
        request = BrandRequestDto(slug=slug)
        response = BrandView.business.get_detail_page(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api
