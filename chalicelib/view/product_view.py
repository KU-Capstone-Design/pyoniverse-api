from chalice import BadRequestError, Blueprint
from dependency_injector.wiring import Provide

from chalicelib.business.interface.business import ProductBusinessIfs
from chalicelib.business.product.dto.request import ProductRequestDto
from chalicelib.view.model.api import Api
from chalicelib.view.model.builder import ApiBuilder


class ProductView:
    api = Blueprint(__name__)
    business: ProductBusinessIfs = Provide["product_business"]

    @staticmethod
    @api.route("/product/{_id}", methods=["GET", "HEAD"], cors=True)
    def get_detail(_id: int) -> Api:
        try:
            request = ProductRequestDto(id=int(_id))
        except Exception:
            raise BadRequestError(f"{_id} should be int type")
        response = ProductView.business.get_detail(request)
        api = (
            ApiBuilder()
            .with_status_code("200 OK")
            .with_status_message("Success")
            .with_data(response)
            .build()
        )
        return api
