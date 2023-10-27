from dataclasses import dataclass

from chalicelib.business.interface.dto import DtoIfs


@dataclass(kw_only=True)
class HomeResponseDto(DtoIfs):
    pass
