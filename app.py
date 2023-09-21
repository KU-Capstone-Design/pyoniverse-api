from chalice import Chalice

from chalicelib.product.product_controller import ProductController


app = Chalice(app_name="pyoniverse-api")
app.api.binary_types.append("application/json")

app.register_blueprint(ProductController.api)
