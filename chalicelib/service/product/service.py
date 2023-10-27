from typing import Literal, Sequence

from chalice import BadRequestError, NotFoundError

from chalicelib.business.interface.service import EventServiceIfs, ProductServiceIfs
from chalicelib.entity.event import EventEntity
from chalicelib.service.interface.command_factory import CommandFactoryIfs
from chalicelib.service.interface.invoker import InvokerIfs


class AsyncProductService(ProductServiceIfs):
    def __init__(self, invoker: InvokerIfs, command_factory: CommandFactoryIfs):
        self.__invoker = invoker
        self.__command_factory = command_factory
        self.__rel_name = "products"
        self.__db_name = "service"

    async def find_chunk(
        self, sort_key: str, direction: Literal["asc", "desc"], chunk_size: int
    ) -> Sequence[EventEntity]:
        if not isinstance(sort_key, str):
            raise BadRequestError(f"{sort_key} should be str type")
        if direction not in {"asc", "desc"}:
            raise BadRequestError(f"{direction} should be in ['asc', 'desc']")
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise BadRequestError(f"{chunk_size} should be int type and >=0")

        if chunk_size <= 10:
            self.__invoker.add_command(
                self.__command_factory.get_sort_by_limit10_command(
                    db_name=self.__db_name,
                    rel_name=self.__rel_name,
                    key=sort_key,
                    value=1 if direction == "asc" else -1,
                )
            )
        else:
            self.__invoker.add_command(
                self.__command_factory.get_select_all_command(
                    db_name=self.__db_name,
                    rel_name=self.__rel_name,
                    key=sort_key,
                    value=1 if direction == "asc" else -1,
                )
            )
        result = (await self.__invoker.invoke())[0]
        if not result:
            raise NotFoundError(f"{self.__db_name}.{self.__rel_name} is empty")
        else:
            return result[:chunk_size]
