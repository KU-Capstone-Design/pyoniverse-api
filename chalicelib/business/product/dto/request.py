from dataclasses import dataclass, field

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class ProductRequestDto(DtoIfs):
    id: int = field(default=None)
