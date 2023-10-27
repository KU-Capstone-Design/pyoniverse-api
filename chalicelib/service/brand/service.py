from chalice import BadRequestError

from chalicelib.business.interface.service import BrandServiceIfs
from chalicelib.entity.brand import BrandEntity
from chalicelib.service.interface.command_factory import CommandFactoryIfs
from chalicelib.service.interface.invoker import InvokerIfs


class AsyncBrandService(BrandServiceIfs):
    def __init__(self, invoker: InvokerIfs, command_factory: CommandFactoryIfs):
        self.__invoker = invoker
        self.__command_factory = command_factory
        self.__rel_name = "brands"
        self.__db_name = "service"

    async def find_by_id(self, entity: BrandEntity) -> BrandEntity:
        if not isinstance(entity, BrandEntity):
            raise BadRequestError("Entity should be BrandEntity")
        if not isinstance(entity.id, int):
            raise BadRequestError(f"{entity.id} should be int type")
        self.__invoker.add_command(
            self.__command_factory.get_equal_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key="id",
                value=entity.id,
            )
        )
        return await self.__invoker.invoke()
