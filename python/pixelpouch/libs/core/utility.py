"""Utility helpers for common patterns and environment variable expansion.

This module provides a thread-safe singleton base class and a helper function
to recursively expand environment variable placeholders in various data
structures.
"""

import os
import re
import threading
from pathlib import Path
from typing import Any, ParamSpec, Self, TypeAlias

P = ParamSpec("P")


class Singleton:
    """Thread-safe singleton base class.

    This class implements a singleton pattern using per-class locks to ensure
    that only one instance of each subclass is created.
    """

    _instances: dict[type, Self] = {}
    _locks: dict[type, threading.Lock] = {}

    def __new__(cls, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Self:
        if cls not in cls._instances:
            lock = cls._locks.setdefault(cls, threading.Lock())
            with lock:
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance

                    init = getattr(cls, "__class_init__", None)
                    if callable(init):
                        init()
        return cls._instances[cls]


TExtractEnvironmentVariablesArg: TypeAlias = (
    dict[str, "TExtractEnvironmentVariablesArg"]
    | list["TExtractEnvironmentVariablesArg"]
    | str
    | Path
)


def extract_environment_variables(
    data: TExtractEnvironmentVariablesArg,
) -> TExtractEnvironmentVariablesArg:
    """Recursively expand environment variable placeholders in the input data.

    This function searches for patterns of the form ``${VAR_NAME}`` and replaces
    them with the corresponding value from ``os.environ``. If an environment
    variable is not defined, the original placeholder is left unchanged.

    Supported input types are dictionaries, lists, strings, and ``Path``
    objects. Nested structures are processed recursively. Values of other
    types are returned as-is.

    Args:
        data: Input data that may contain environment variable placeholders.

    Returns:
        The input data with environment variable placeholders expanded, while
        preserving the original data structure and types where possible.
    """
    pattern = re.compile(r"\${(\w+)}")

    if isinstance(data, dict):
        return {
            key: extract_environment_variables(value) for key, value in data.items()
        }
    elif isinstance(data, list):
        return [extract_environment_variables(item) for item in data]
    elif isinstance(data, str):
        return pattern.sub(lambda x: os.environ.get(x.group(1), x.group(0)), data)
    elif isinstance(data, Path):
        old_path = str(data)
        new_path = pattern.sub(
            lambda x: os.environ.get(x.group(1), x.group(0)), old_path
        )
        if new_path == old_path:
            return data
        return Path(new_path)
    else:
        return data
