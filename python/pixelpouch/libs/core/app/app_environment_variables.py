"""Base utilities for reading and validating application environment variables.

This module defines an abstract base class that provides typed helper methods
for reading environment variables from a mapping. It centralizes common parsing
and validation logic for strings, paths, booleans, numbers, and enums, and
provides a dedicated exception type for environment-related errors.
"""

from __future__ import annotations

import os
from abc import ABC
from distutils.util import strtobool
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Type, TypeVar

if TYPE_CHECKING:
    from collections.abc import Mapping

_TEnum = TypeVar("_TEnum", bound=Enum)


class EnvironmentVariableError(RuntimeError):
    """Error raised when an environment variable is missing or invalid.

    This exception is used to signal configuration issues related to
    environment variables, such as missing values or type conversion failures.
    """


class AppEnvironmentVariables(ABC):
    """Abstract base class for accessing application environment variables.

    This class provides reusable helper methods for reading and converting
    environment variable values into strongly typed Python objects. Subclasses
    are expected to define their own public attributes using these helpers.
    """

    def __init__(self, env: Optional[Mapping[str, str]] = None) -> None:
        """Initialize the environment variable accessor.

        Args:
            env: Optional mapping of environment variables. If ``None``,
                ``os.environ`` is used.
        """
        self._env: Mapping[str, str] = env if env is not None else os.environ

    @classmethod
    def _read_str(cls, env: Mapping[str, str], key: str) -> str:
        """Read a required string environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            The string value of the environment variable.

        Raises:
            EnvironmentVariableError: If the variable is not defined.
        """
        value = env.get(key)
        if value is None:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' is not defined."
            )
        return value

    @classmethod
    def _read_str_opt(
        cls,
        env: Mapping[str, str],
        key: str,
    ) -> str | None:
        """Read an optional string environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            The string value of the environment variable if defined,
            otherwise ``None``.
        """
        value = env.get(key)
        if value is None:
            return None
        return value

    @classmethod
    def _read_path(cls, env: Mapping[str, str], key: str) -> Path:
        """Read a required path environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            A ``Path`` constructed from the environment variable value.

        Raises:
            EnvironmentVariableError: If the variable is not defined.
        """
        return Path(cls._read_str(env, key))

    @classmethod
    def _read_path_list(
        cls,
        env: Mapping[str, str],
        key: str,
        separator: str = ";",
        remove_empty_or_whitespace: bool = True,
    ) -> list[Path]:
        """Read an optional list of paths from an environment variable.

        The variable value is split using the specified separator and each
        element is converted to a ``Path``.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.
            separator: Separator used to split the value.
            remove_empty_or_whitespace: Whether to ignore empty or whitespace-only
                entries.

        Returns:
            A list of ``Path`` objects. Returns an empty list if the variable
            is not defined.
        """
        value = env.get(key)
        if value is None:
            return []

        return [
            Path(path)
            for path in value.split(separator)
            if not remove_empty_or_whitespace or path.strip()
        ]

    @classmethod
    def _read_bool_opt(cls, env: Mapping[str, str], key: str) -> Optional[bool]:
        """Read an optional boolean environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            ``True`` or ``False`` if the variable is defined, otherwise ``None``.

        Raises:
            EnvironmentVariableError: If the value cannot be interpreted
                as a boolean.
        """
        value = env.get(key)
        if value is None:
            return None

        value = value.strip()
        if not value:
            return False

        try:
            return bool(strtobool(value))
        except ValueError as e:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' must be a boolean, got '{value}'."
            ) from e

    @classmethod
    def _read_bool(cls, env: Mapping[str, str], key: str) -> bool:
        """Read a required boolean environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            Boolean value of the environment variable.

        Raises:
            EnvironmentVariableError: If the variable is missing or cannot
                be interpreted as a boolean.
        """
        value = env.get(key)
        if value is None:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' is not defined."
            )

        value = value.strip()
        if not value:
            return False

        try:
            return bool(strtobool(value))
        except ValueError as e:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' must be a boolean, got '{value}'."
            ) from e

    @classmethod
    def _read_enum_opt(
        cls,
        env: Mapping[str, str],
        key: str,
        enum_type: Type[_TEnum],
    ) -> Optional[_TEnum]:
        """Read an optional enum-valued environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.
            enum_type: Enum type used to convert the value.

        Returns:
            An enum value if the variable is defined, otherwise ``None``.

        Raises:
            TypeError: If ``enum_type`` is not a subclass of ``Enum``.
            EnvironmentVariableError: If the value cannot be converted to
                the specified enum.
        """
        if not issubclass(enum_type, Enum):
            raise TypeError(f"'{enum_type}' is not a subclass of Enum.")

        value = env.get(key)
        if value is None:
            return None

        try:
            return enum_type(value)
        except ValueError as e:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' must be one of "
                f"{[e.value for e in enum_type]}, got '{value}'."
            ) from e

    @classmethod
    def _read_int(cls, env: Mapping[str, str], key: str) -> int:
        """Read a required integer environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            Integer value of the environment variable.

        Raises:
            EnvironmentVariableError: If the variable is missing or cannot
                be converted to an integer.
        """
        value = cls._read_str(env, key)
        try:
            return int(value)
        except ValueError as e:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' must be an integer, got '{value}'."
            ) from e

    @classmethod
    def _read_int_opt(cls, env: Mapping[str, str], key: str) -> Optional[int]:
        """Read an optional integer environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            Integer value if defined, otherwise ``None``.

        Raises:
            EnvironmentVariableError: If the value cannot be converted
                to an integer.
        """
        value = env.get(key)
        if value is None:
            return None

        value = value.strip()
        if not value:
            return None

        try:
            return int(value)
        except ValueError as e:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' must be an integer, got '{value}'."
            ) from e

    @classmethod
    def _read_float(cls, env: Mapping[str, str], key: str) -> float:
        """Read a required float environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            Float value of the environment variable.

        Raises:
            EnvironmentVariableError: If the variable is missing or cannot
                be converted to a float.
        """
        value = cls._read_str(env, key)
        try:
            return float(value)
        except ValueError as e:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' must be a float, got '{value}'."
            ) from e

    @classmethod
    def _read_float_opt(cls, env: Mapping[str, str], key: str) -> Optional[float]:
        """Read an optional float environment variable.

        Args:
            env: Environment variable mapping.
            key: Environment variable name.

        Returns:
            Float value if defined, otherwise ``None``.

        Raises:
            EnvironmentVariableError: If the value cannot be converted
                to a float.
        """
        value = env.get(key)
        if value is None:
            return None

        value = value.strip()
        if not value:
            return None

        try:
            return float(value)
        except ValueError as e:
            raise EnvironmentVariableError(
                f"Environment variable '{key}' must be a float, got '{value}'."
            ) from e
