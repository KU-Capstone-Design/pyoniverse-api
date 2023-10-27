from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.entity.base import EntityType


class ProductConverter(ConverterIfs):
    def convert_to_entity(self, dto: DtoType) -> EntityType:
        pass

    def convert_to_dto(self, entity: EntityType) -> DtoType:
        pass
