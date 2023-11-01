import gzip
import traceback
from typing import Any, Dict, Literal, Optional

from chalice.app import Chalice, Request, Response, RestAPIEventHandler
from overrides import override

from chalicelib.view.brand_view import BrandView
from chalicelib.view.event_view import EventView
from chalicelib.view.home_view import HomeView
from chalicelib.view.model.builder import ApiBuilder
from chalicelib.view.model.serializer import JsonSerializer
from chalicelib.view.product_view import ProductView
from chalicelib.view.search_view import SearchView


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
        prefix = f"/{version}"

        self.register_blueprint(BrandView.api, url_prefix=prefix)
        self.register_blueprint(HomeView.api, url_prefix=prefix)
        self.register_blueprint(EventView.api, url_prefix=prefix)
        self.register_blueprint(SearchView.api, url_prefix=prefix)
        self.register_blueprint(ProductView.api, url_prefix=prefix)


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
