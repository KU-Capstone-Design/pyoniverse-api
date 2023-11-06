import logging

import dotenv

from chalicelib.converter.brand import BrandConverter
from chalicelib.converter.event import EventConverter
from chalicelib.converter.home import HomeConverter
from chalicelib.converter.metric import MetricConverter
from chalicelib.converter.product import ProductConverter
from chalicelib.converter.search import SearchConverter
from chalicelib.extern.dependency_injector.business import BusinessInjector
from chalicelib.extern.dependency_injector.persistant import PersistentInjector
from chalicelib.extern.dependency_injector.resource import ResourceInjector
from chalicelib.extern.dependency_injector.service import (
    ServiceInjector as TmpServiceInjector,
)


class MainInjector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            # is_injected를 init에서 초기화하면 객체가 싱글톤이어도 init은 계속 호출되기 때문에 초기화가 매번 발생된다.
            cls.__instance.__is_injected = False
            cls.__instance.injectors = {}
            # Resource Initialize
            cls.__instance.__resource_injector = ResourceInjector()
            cls.__instance.__resource_injector.init_resources()
            # Set logger
            cls.__instance.logger = logging.getLogger(__name__)
        return cls.__instance

    def __init__(self):
        pass

    def inject(self):
        if self.__is_injected:
            self.logger.info("Dependencies are already injected")
            return
        self.__is_injected = True
        self.__configure()
        self.logger.info("Inject Dependencies")
        client = self.__resource_injector.client()
        self.injectors["persistent"] = PersistentInjector(client=client)
        self.injectors["persistent"].check_dependencies()

        self.injectors["service"] = TmpServiceInjector(
            command_factory=self.injectors["persistent"].command_factory(),
            brand_invoker=self.injectors["persistent"].invoker(),
            constant_brand_invoker=self.injectors["persistent"].invoker(),
            product_invoker=self.injectors["persistent"].invoker(),
            event_invoker=self.injectors["persistent"].invoker(),
        )
        self.injectors["service"].check_dependencies()

        self.injectors["business"] = BusinessInjector(
            loop=client.get_io_loop(),
            home_converter=HomeConverter(),
            brand_converter=BrandConverter(),
            event_converter=EventConverter(),
            search_converter=SearchConverter(),
            product_converter=ProductConverter(),
            metric_converter=MetricConverter(),
            brand_service=self.injectors["service"].brand_service(),
            constant_brand_service=self.injectors["service"].constant_brand_service(),
            event_service=self.injectors["service"].event_service(),
            product_service=self.injectors["service"].product_service(),
        )
        self.injectors["business"].check_dependencies()
        return self.injectors

    def __configure(self):
        """
        환경 변수 등의 사전 설정
        :return:
        """
        dotenv.load_dotenv()
