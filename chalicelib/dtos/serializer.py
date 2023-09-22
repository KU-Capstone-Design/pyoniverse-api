import json
from dataclasses import fields, is_dataclass
from typing import Mapping


class JsonSerializer:
    """
    Change '-' to '_' in key
    """

    @staticmethod
    def serialize(obj: Mapping) -> str:
        res = JsonSerializer.__serialize(obj)
        return json.dumps(res, ensure_ascii=False)

    @staticmethod
    def __serialize(obj: Mapping) -> dict:
        res = {}
        if is_dataclass(obj):
            for _field in fields(obj):
                key = _field.name.replace("-", "_")
                value = getattr(obj, _field.name)
                if is_dataclass(value) or isinstance(value, dict):
                    value = JsonSerializer.__serialize(value)
                if isinstance(value, list):
                    value = [JsonSerializer.__serialize(v) for v in value]
                res[key] = value
        elif isinstance(obj, dict):
            for key, value in obj.items():
                key = key.replace("-", "_")
                if is_dataclass(value) or isinstance(value, dict):
                    value = JsonSerializer.__serialize(value)
                if isinstance(value, list):
                    value = [JsonSerializer.__serialize(v) for v in value]
                res[key] = value
        else:
            raise TypeError(f"obj is not dataclass or dict: {obj}")
        return res
