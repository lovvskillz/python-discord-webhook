from typing import Any, Type


def to_dict(value: Any) -> Any:
    """
    Convert objects and nested values to JSON serializable data.
    :param value: value that should be converted
    :return: converted value
    """
    if isinstance(value, list):
        return [to_dict(item) for item in value]
    if isinstance(value, dict):
        return {key: to_dict(item) for key, item in value.items() if item is not None}
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return value


def is_int(value: Any) -> bool:
    """
    Check whether the given value is an integer. Booleans are not accepted.
    :param value: value that should be checked
    :return: whether the value is an integer
    """
    return isinstance(value, int) and not isinstance(value, bool)


def check_max_length(
    value: Any, max_length: int, name: str, exception: Type[Exception]
) -> None:
    """
    Raise the given exception if the value exceeds the maximum length.
    :param value: value that should be checked
    :param int max_length: maximum amount of characters
    :param str name: name of the field that is being checked
    :param exception: exception that should be raised
    """
    if value is not None and len(value) > max_length:
        raise exception(f"{name} can be a maximum of {max_length} characters.")
