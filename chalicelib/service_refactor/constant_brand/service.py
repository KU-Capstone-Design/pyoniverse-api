from typing import Sequence

from chalicelib.business.interface.service import ConstantBrandServiceIfs
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.service_refactor.interface.factory import FactoryIfs
from chalicelib.service_refactor.interface.service import AbstractService
from chalicelib.service_refactor.model.enum import OperatorEnum


class AsyncConstantBrandService(ConstantBrandServiceIfs, AbstractService):
    def __init__(self, factory: FactoryIfs):
        super().__init__(factory)
        self.__rel_name = "brands"
        self.__db_name = "constant"

    async def find_all(self) -> Sequence[ConstantBrandEntity]:
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.read()
        return result.get()

    async def find_by_slug(self, entity: ConstantBrandEntity) -> ConstantBrandEntity:
        builder = self._factory.make(db=self.__db_name, rel=self.__rel_name)
        result = await builder.where(OperatorEnum.EQUAL, "slug", entity.slug).read()
        return result.get()
