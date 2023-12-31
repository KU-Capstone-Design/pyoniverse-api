from abc import ABCMeta, abstractmethod
from typing import Type

from chalicelib.business.interface.dto import DtoType
from chalicelib.entity.base import EntityType


class ConverterIfs(metaclass=ABCMeta):
    @abstractmethod
    def convert_to_entity(self, dto: DtoType) -> EntityType:
        pass

    @abstractmethod
    def convert_to_dto(self, entity: EntityType, dto_type: Type[DtoType]) -> DtoType:
        pass
