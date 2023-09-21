from typing import Type

from chalice import Blueprint

from chalicelib.factories.service_factory import ServiceFactory
from chalicelib.interfaces.controller import Controller
from chalicelib.interfaces.service import Service


class HomeController(Controller):
    api = Blueprint(__name__)
    service: Type[Service] = ServiceFactory.create_service("home_service")

    @staticmethod
    @api.route("/", methods=["GET", "HEAD"], cors=True)
    def index():
        return {"message": "Welcome to Pyoniverse API!"}
