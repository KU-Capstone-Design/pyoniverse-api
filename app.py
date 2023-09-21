from chalice import Chalice

from chalicelib.home.home_controller import HomeController


app = Chalice(app_name="pyoniverse-api")
app.api.binary_types.append("application/json")

app.register_blueprint(HomeController.api, url_prefix="/home")
