import gzip
import traceback
from typing import Any, Dict, Literal, Optional

from chalice.app import Chalice, Request, Response, RestAPIEventHandler
from overrides import override

from chalicelib.common.model.builder import ApiBuilder
from chalicelib.common.model.serializer import JsonSerializer


class CustomChalice(Chalice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override
    def __call__(self, event: Any, context: Any) -> Dict[str, Any]:
        self.lambda_context = context
        # Use CustomRestAPIEventHandler instead of RestAPIEventHandler
        handler = CustomRestAPIEventHandler(
            self.routes,
            self.api,
            self.log,
            self.debug,
            middleware_handlers=self._get_middleware_handlers("http"),
        )
        self.current_request: Optional[Request] = handler.create_request_object(
            event, context
        )
        return handler(event, context)

    def register_controller(self, version: Literal["v1"]) -> None:
        """
        :param version: v1
        :return:
        """
        from chalicelib.domain.brand.brand_controller import BrandController
        from chalicelib.domain.event.event_controller import EventController
        from chalicelib.domain.home.home_controller import HomeController
        from chalicelib.domain.product.product_controller import ProductController

        prefix = f"/{version}"

        self.register_blueprint(HomeController.api, url_prefix=prefix)
        self.register_blueprint(BrandController.api, url_prefix=prefix)
        # from chalicelib.view.brand_view import BrandView

        # self.register_blueprint(BrandView.api, url_prefix=prefix)
        self.register_blueprint(EventController.api, url_prefix=prefix)
        self.register_blueprint(ProductController.api, url_prefix=prefix)


class CustomRestAPIEventHandler(RestAPIEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override
    def _unhandled_exception_to_response(self) -> Response:
        encoded_header = {
            "Content-Type": "application/json",
            "Content-Encoding": "gzip",
        }
        path = getattr(self.current_request, "path", "unknown")
        self.log.error("Caught exception for path %s", path, exc_info=True)
        if self.debug:
            stack_trace = "".join(traceback.format_exc())
            msg: Any = stack_trace
            body = ApiBuilder().with_status_code("500").with_status_message(msg).build()
        else:
            msg = "An internal server error occurred."
            body = ApiBuilder().with_status_code("500").with_status_message(msg).build()

        # 최상위 Exception을 잡아서 처리하므로, serializer, gzip 등의 middleware를 거치지 않음
        body = JsonSerializer.serialize(body)
        body = gzip.compress(body.encode("utf-8"))
        response = Response(body=body, headers=encoded_header, status_code=500)
        return response
