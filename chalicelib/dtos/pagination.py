from dataclasses import dataclass, field

from chalicelib.dtos.serializer import JsonSerializer


@dataclass
class Pagination:
    page: int = field()
    size: int = field()
    total_size: int = field()
    total_page: int = field()
    sort: str = field()
    direction: str = field()
    filter: str = field()

    def to_dict(self):
        return JsonSerializer.serialize(self)
