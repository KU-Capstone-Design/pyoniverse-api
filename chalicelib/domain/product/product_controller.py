from chalice import Blueprint
from dependency_injector.wiring import Provide

from chalicelib.domain.product.product_service import ProductService
from chalicelib.interface.controller import Controller


class ProductController(Controller):
    api = Blueprint(__name__)
    service: ProductService = Provide["product_service"]
