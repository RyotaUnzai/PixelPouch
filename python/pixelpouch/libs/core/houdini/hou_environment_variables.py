"""Environment variable definitions and accessors for Houdini integration.

This module defines strongly typed environment variable keys and a concrete
accessor class for Houdini-related environment variables. Centralizing these
definitions avoids hard-coded strings and provides consistent parsing and
typing for paths and path lists used by the application.
"""

import os
from collections.abc import Mapping, Sequence
from enum import StrEnum, unique
from pathlib import Path
from typing import Optional

from pixelpouch.libs.core.app import AppEnvironmentVariables


@unique
class HoudiniEnvironmentVariableKey(StrEnum):
    """String enumeration of supported Houdini environment variable keys.

    Each enum member represents the exact name of an environment variable
    expected to be present in the runtime environment.
    """

    HOUDINI_LOCATION = "HOUDINI_LOCATION"
    HYTHON_LOCATION = "HYTHON_LOCATION"
    HOUDINI_PATH = "HOUDINI_PATH"
    HOUDINI_TOOLBAR_PATH = "HOUDINI_TOOLBAR_PATH"


class HoudiniEnvironmentVariables(AppEnvironmentVariables):
    """Accessor for Houdini-related environment variables.

    This class reads and exposes Houdini-specific environment variables via
    typed properties. Parsing and validation are delegated to the base
    AppEnvironmentVariables implementation.
    """

    def __init__(self, env: Optional[Mapping[str, str]] = None) -> None:
        """Initializes the Houdini environment variable reader.

        Args:
            env: Optional mapping of environment variables. If not provided,
                ``os.environ`` is used.
        """
        env = env if env is not None else os.environ
        super().__init__(env)

        self.__HOUDINI_LOCATION: Path = self._read_path(
            env, HoudiniEnvironmentVariableKey.HOUDINI_LOCATION
        )
        self.__HYTHON_LOCATION: Path = self._read_path(
            env, HoudiniEnvironmentVariableKey.HYTHON_LOCATION
        )
        self.__HOUDINI_PATH: Sequence[Path] = self._read_path_list(
            env, HoudiniEnvironmentVariableKey.HOUDINI_PATH
        )
        self.__HOUDINI_TOOLBAR_PATH: Sequence[Path] = self._read_path_list(
            env, HoudiniEnvironmentVariableKey.HOUDINI_TOOLBAR_PATH
        )

    @property
    def HOUDINI_LOCATION(self) -> Path:
        """Returns the Houdini installation directory.

        Returns:
            The Houdini installation path as a Path object.
        """
        return self.__HOUDINI_LOCATION

    @property
    def HYTHON_LOCATION(self) -> Path:
        """Returns the Hyton executable location.

        Returns:
            The Hyton executable path as a Path object.
        """
        return self.__HYTHON_LOCATION

    @property
    def HOUDINI_PATH(self) -> Sequence[Path]:
        """Returns the list of Houdini search paths.

        Returns:
            A sequence of paths configured in the HOUDINI_PATH environment
            variable.
        """
        return self.__HOUDINI_PATH

    @property
    def HOUDINI_TOOLBAR_PATH(self) -> Sequence[Path]:
        """Returns the list of Houdini toolbar search paths.

        Returns:
            A sequence of paths configured in the HOUDINI_TOOLBAR_PATH
            environment variable.
        """
        return self.__HOUDINI_TOOLBAR_PATH
