from chalice import BadRequestError
from overrides import override

from chalicelib.interface.service import Service


class BrandService(Service):
    def get_single(self, **kwargs) -> object:
        brand = self._repository.find_by_slug(kwargs["slug"])
        if not brand:
            raise BadRequestError(f"Invalid slug: {kwargs['slug']}")
        return brand
