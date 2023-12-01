import enum


@enum.unique
class OperatorEnum(enum.Enum):
    NOT = enum.auto()
    EQUAL = enum.auto()
    GREATER_THAN = enum.auto()
    LESS_THAN = enum.auto()
    GREATER_OR_EQUAL_THAN = enum.auto()
    LESS_OR_EQUAL_THAN = enum.auto()
    IN = enum.auto()
    NOT_IN = enum.auto()
