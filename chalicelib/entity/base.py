from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class BaseEntity:
    id: int = field(default=None)
    status: int = field(default=None)
    created_at: datetime = field(default=None)
    updated_at: datetime = field(default=None)
