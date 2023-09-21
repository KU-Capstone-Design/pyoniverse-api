from dataclasses import dataclass, fields, is_dataclass


class JsonSerializer:
    """
    Change '-' to '_' in key
    """

    @staticmethod
    def serialize(obj: dataclass) -> dict:
        res = {}
        for _field in fields(obj):
            key = _field.name.replace("-", "_")
            value = getattr(obj, _field.name)
            if is_dataclass(value):
                value = JsonSerializer.serialize(value)
            res[key] = value
        return res
