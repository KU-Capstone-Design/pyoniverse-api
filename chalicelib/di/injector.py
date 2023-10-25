from chalicelib.di.db.adaptor import DBAdaptorInjector
from chalicelib.di.db.repository import RepositoryInjector
from chalicelib.di.service.service import ServiceInjector


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
