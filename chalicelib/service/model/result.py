from typing import List

from chalicelib.entity.base import EntityType


class Result:
    def __init__(self, data: EntityType | List[EntityType]):
        self.__data = data

    def get(self) -> EntityType | List[EntityType]:
        return self.__data
