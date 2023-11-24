from dataclasses import dataclass, field


@dataclass
class Pagination:
    page: int = field()
    size: int = field()
    total_size: int = field()
    total_page: int = field()
    sort: str = field()
    direction: str = field()
    filter: str = field()
