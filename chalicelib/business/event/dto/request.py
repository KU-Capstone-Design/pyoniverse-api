from dataclasses import dataclass, field

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class EventRequestDto(DtoIfs):
    brand_slug: str = field(default=None)
    id: int = field(default=None)
