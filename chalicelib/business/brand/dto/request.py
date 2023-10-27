from dataclasses import dataclass, field

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class BrandRequestDto(DtoIfs):
    id: int = field(default=None)
