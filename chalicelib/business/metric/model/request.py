from dataclasses import dataclass, field

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class MetricRequestDto(DtoIfs):
    domain: str = field(default=None)
    id: int = field(default=None)
    value: int = field(default=None)
