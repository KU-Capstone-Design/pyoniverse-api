from chalice import BadRequestError, NotFoundError

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

    async def find_by_slug(self, entity: BrandEntity) -> BrandEntity:
        if not isinstance(entity, BrandEntity):
            raise BadRequestError("Entity should be BrandEntity")
        if not isinstance(entity.slug, str):
            raise BadRequestError(f"{entity.slug} should be str type")
        self.__invoker.add_command(
            self.__command_factory.get_equal_command(
                db_name=self.__db_name,
                rel_name=self.__rel_name,
                key="slug",
                value=entity.slug,
            )
        )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(
                f"{entity.id} not in {self.__db_name}.{self.__rel_name}"
            )
        else:
            return result
