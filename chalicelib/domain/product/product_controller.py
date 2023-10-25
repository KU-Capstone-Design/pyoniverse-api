from chalice import Blueprint
from dependency_injector.wiring import Provide

from chalicelib.interface.controller import Controller
from chalicelib.interface.service import Service


class ProductController(Controller):
    api = Blueprint(__name__)
    service: Service = Provide["product_service"]
