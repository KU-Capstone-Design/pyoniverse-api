from dotenv import load_dotenv


load_dotenv()
import os

from chalice import BadRequestError

from chalicelib.chalice import CustomChalice
from chalicelib.domain.home.home_controller import HomeController
from chalicelib.domain.brand.brand_controller import BrandController
from chalicelib.middlewares.error_handler import handle_errors
from chalicelib.middlewares.response_handler import handle_response


if os.getenv("LOG_LEVEL", "DEBUG") == "DEBUG":
    debug = True
else:
    debug = False

app = CustomChalice(app_name="pyoniverse-api", debug=debug)
app.api.binary_types.append("application/json")

app.register_blueprint(HomeController.api, url_prefix="/v1")
app.register_blueprint(BrandController.api, url_prefix="/v1")

app.register_middleware(handle_response, "http")
app.register_middleware(handle_errors, "http")


@app.route("/error")
def error():
    raise BadRequestError("asdf")
