import os

from chalicelib.chalice import CustomChalice
from chalicelib.extern.dependency_injector.injector import MainInjector
from chalicelib.extern.middleware.error_handler import handle_errors
from chalicelib.extern.middleware.response_handler import handle_response


if os.getenv("LOG_LEVEL", "DEBUG") == "DEBUG":
    debug = True
else:
    debug = False

main_injector = MainInjector()
main_injector.inject()

app = CustomChalice(app_name="pyoniverse-api", debug=debug)

app.register_controller(version="v1")
app.register_middleware(handle_response, "http")
app.register_middleware(handle_errors, "http")
