import os

import dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.business.brand.converter import BrandConverter
from chalicelib.dependency_injector.business import BusinessInjector
from chalicelib.dependency_injector.db.adaptor import DBAdaptorInjector
from chalicelib.dependency_injector.db.repository import RepositoryInjector
from chalicelib.dependency_injector.persistant import PersistentInjector
from chalicelib.dependency_injector.service.service import ServiceInjector
from chalicelib.dependency_injector.tmp_service import (
    ServiceInjector as TmpServiceInjector,
)


class MainInjector:
    def __init__(self):
        self.injectors = {}

    def inject(self):
        adaptor_injector = DBAdaptorInjector()
        repository_injector = RepositoryInjector(
            adaptor=adaptor_injector.mongo_adaptor()
        )
        service_injector = ServiceInjector(
            home_repository=repository_injector.home_repository(),
            brand_repository=repository_injector.brand_repository(),
            event_repository=repository_injector.event_repository(),
            product_repository=repository_injector.product_repository(),
        )
        self.injectors["adaptor"] = adaptor_injector
        self.injectors["repository"] = repository_injector
        self.injectors["service"] = service_injector


class TmpMainInjector:
    def __init__(self):
        self.__configure()
        self.injectors = {}

    def inject(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        self.injectors["persistent"] = PersistentInjector(client=client)
        self.injectors["service"] = TmpServiceInjector(
            command_factory=self.injectors["persistent"].command_factory(),
            invoker=self.injectors["persistent"].invoker(),
        )
        self.injectors["business"] = BusinessInjector(
            loop=client.get_io_loop(),
            brand_converter=BrandConverter(),
            brand_service=self.injectors["service"].brand_service(),
        )
        return self.injectors

    def __configure(self):
        """
        환경 변수 등의 사전 설정
        :return:
        """
        dotenv.load_dotenv()
