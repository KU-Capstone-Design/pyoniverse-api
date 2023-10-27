from typing import Sequence

from chalice import NotFoundError

from chalicelib.business.interface.service import ConstantBrandServiceIfs
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.service.interface.command_factory import CommandFactoryIfs
from chalicelib.service.interface.invoker import InvokerIfs


class AsyncBrandService(ConstantBrandServiceIfs):
    def __init__(self, invoker: InvokerIfs, command_factory: CommandFactoryIfs):
        self.__invoker = invoker
        self.__command_factory = command_factory
        self.__rel_name = "brands"
        self.__db_name = "constant"

    async def find_all(self) -> Sequence[ConstantBrandEntity]:
        self.__invoker.add_command(
            self.__command_factory.get_select_all_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(f"{self.__db_name}.{self.__rel_name} is empty")
        else:
            return result
