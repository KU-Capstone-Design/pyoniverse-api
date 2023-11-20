import logging
from functools import lru_cache
from typing import Sequence

import aiohttp
from chalice import BadRequestError, ChaliceViewError

from chalicelib.business.interface.service import SearchServiceIfs
from chalicelib.service.search.model.search_engine_response import (
    SearchEngineResponseDto,
)


class AsyncSearchService(SearchServiceIfs):
    def __init__(self, engine_uri: str):
        self.__engine_uri = engine_uri
        assert self.__engine_uri
        self.logger = logging.getLogger(__name__)

    @lru_cache(maxsize=512)
    async def find_products(self, query: str) -> Sequence[int]:
        if not query:
            raise BadRequestError(f"{query} should be not empty")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.__engine_uri}/search/{query}") as response:
                if response.status == 404:
                    body = SearchEngineResponseDto(results=[])
                elif response.status != 404 and not response.ok:
                    self.logger.error(await response.text())
                    raise ChaliceViewError("Search Request Timeout")
                else:
                    raw_body = await response.json()
                    body = SearchEngineResponseDto(
                        version=raw_body["data"]["version"],
                        engine_type=raw_body["data"]["engine_type"],
                        results=raw_body["data"]["results"],
                    )
                self.logger.info(f"Search Result(query={query}): {body}")
                return body.results
