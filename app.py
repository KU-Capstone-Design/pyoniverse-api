from chalice import Chalice

from chalicelib.home.home_controller import HomeController
from chalicelib.middlewares.error_handler import handle_errors
from chalicelib.middlewares.response_handler import handle_response


app = Chalice(app_name="pyoniverse-api")
app.api.binary_types.append("application/json")

app.register_blueprint(HomeController.api, url_prefix="/v1")

app.register_middleware(handle_response, "http")
app.register_middleware(handle_errors, "http")


@app.route("/error")
def error():
    raise Exception()
