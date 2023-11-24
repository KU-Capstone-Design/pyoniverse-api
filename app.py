import logging
import os

from chalicelib.chalice import CustomChalice
from chalicelib.extern.dependency_injector.injector import MainInjector
from chalicelib.extern.middleware.error_handler import handle_errors
from chalicelib.extern.middleware.response_handler import handle_response


main_injector = MainInjector()
main_injector.inject()

if os.getenv("LOG_LEVEL", "DEBUG") == "DEBUG":
    logging.basicConfig(level=logging.DEBUG, force=True)
else:
    logging.basicConfig(level=logging.INFO, force=True)

app = CustomChalice(app_name="pyoniverse-api")

app.register_controller(version="v1")
app.register_middleware(handle_response, "http")
app.register_middleware(handle_errors, "http")
