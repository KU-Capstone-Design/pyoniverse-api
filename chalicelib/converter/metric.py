from typing import Type

from chalicelib.business.interface.converter import ConverterIfs
from chalicelib.business.interface.dto import DtoType
from chalicelib.business.metric.model.request import MetricRequestDto
from chalicelib.business.metric.model.response import MetricResponseDto
from chalicelib.entity.base import EntityType


class MetricConverter(ConverterIfs):
    def convert_to_entity(self, dto: MetricRequestDto) -> EntityType:
        raise NotImplementedError

    def convert_to_dto(
        self, entity: EntityType, dto_type: Type[DtoType]
    ) -> MetricResponseDto:
        raise NotImplementedError
