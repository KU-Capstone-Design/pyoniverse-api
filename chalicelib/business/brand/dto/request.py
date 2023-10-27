from dataclasses import dataclass, field

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class BrandRequestDto(DtoIfs):
    slug: str = field(default=None)
