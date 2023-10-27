from asyncio import gather
from typing import Sequence

from chalicelib.entity.base import EntityType
from chalicelib.service.interface.invoker import InvokerIfs


class AsyncInvoker(InvokerIfs):
    async def invoke(self) -> Sequence[Sequence[EntityType] | EntityType | None]:
        result = await gather(*[c.execute() for c in self._commands])
        self._commands = []  # command 초기화
        return result
