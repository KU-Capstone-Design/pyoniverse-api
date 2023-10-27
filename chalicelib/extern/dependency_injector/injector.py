import logging
import os

import dotenv
from motor.motor_asyncio import AsyncIOMotorClient

from chalicelib.converter.brand import BrandConverter
from chalicelib.converter.event import EventConverter
from chalicelib.converter.home import HomeConverter
from chalicelib.extern.dependency_injector.business import BusinessInjector
from chalicelib.extern.dependency_injector.persistant import PersistentInjector
from chalicelib.extern.dependency_injector.service import (
    ServiceInjector as TmpServiceInjector,
)


class MainInjector:
    def __init__(self):
        self.__configure()
        self.injectors = {}

    def inject(self):
        logging.info("Inject Dependencies")
        client = self.__get_client()
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

    def __get_client(self):
        client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        client.get_io_loop().run_until_complete(client.admin.command("ping"))
        return client
