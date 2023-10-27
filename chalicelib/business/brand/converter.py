from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.entity.base import EntityType


class BrandConverter(ConverterIfs):
    def convert_to_dto(self, entity: EntityType) -> DtoType:
        pass

    def convert_to_entity(self, dto: DtoType) -> EntityType:
        pass
