from asyncio import Future, gather
from typing import Sequence

from chalicelib.entity.base import EntityType
from chalicelib.service.interface.invoker import InvokerIfs


class AsyncInvoker(InvokerIfs):
    async def invoke(self) -> Future[Sequence[EntityType] | EntityType | None]:
        return gather(*self._commands)
