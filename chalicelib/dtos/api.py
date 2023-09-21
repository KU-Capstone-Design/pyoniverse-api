from dataclasses import dataclass, field
from typing import List, Optional

from chalicelib.dtos.serializer import JsonSerializer
from chalicelib.dtos.pagination import Pagination


@dataclass
class Api:
    status_code: str = field()
    status_message: str = field()
    data: dict = field()
    errors: Optional[List[str]] = field(default=None)
    pagination: Optional[Pagination] = field(default=None)

    def to_dict(self):
        return JsonSerializer.serialize(self)
