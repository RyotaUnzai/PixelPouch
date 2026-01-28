"""Definitions of environment variable keys used by the PixelPouch application.

This module defines strongly typed environment variable keys and a concrete
environment variable accessor class. Centralizing environment variable names
and access logic avoids hard-coded strings and ensures consistent parsing of
environment values across the codebase.
"""

import os
from collections.abc import Mapping
from enum import StrEnum, unique
from pathlib import Path
from typing import Optional

from pixelpouch.libs.core.app import AppEnvironmentVariables


@unique
class PixelPouchEnv(StrEnum):
    """Enumeration of supported PixelPouch runtime environments.

    This enum represents the logical execution environment of the application
    and is typically used to switch behavior between development and release
    configurations.
    """

    DEV = "dev"
    RELEASE = "release"


@unique
class ExecutionContextEnv(StrEnum):
    VSCODE = "vscode"
    HOUDINI = "houdini"
    MAYA = "maya"


@unique
class EnvironmentVariableKey(StrEnum):
    """String enumeration of supported environment variable keys.

    Each enum member corresponds to the exact name of an environment variable
    expected to exist in the runtime environment. Using a StrEnum provides
    type safety while preserving compatibility with APIs expecting strings.
    """

    LOCALAPPDATA = "LOCALAPPDATA"
    USERPROFILE = "USERPROFILE"
    PIXELPOUCH_LOCATION = "PIXELPOUCH_LOCATION"
    PIXELPOUCH_ENV = "PIXELPOUCH_ENV"
    PIXELPOUCH_EXECUTION_CONTEXT = "PIXELPOUCH_EXECUTION_CONTEXT"

    # dev-only
    PIXELPOUCH_DEBUGGER_ENABLE = "PIXELPOUCH_DEBUGGER_ENABLE"
    PIXELPOUCH_HOST = "PIXELPOUCH_HOST"
    PIXELPOUCH_PORT = "PIXELPOUCH_PORT"


class PixelPouchEnvironmentVariables(AppEnvironmentVariables):
    """Accessor for PixelPouch-related environment variables.

    This class reads, validates, and exposes required PixelPouch environment
    variables via typed properties. It delegates low-level parsing and error
    handling to the base AppEnvironmentVariables implementation.
    """

    def __init__(self, env: Optional[Mapping[str, str]] = None) -> None:
        """Initializes the environment variable reader.

        Args:
            env: Optional mapping of environment variables. If not provided,
                ``os.environ`` is used.
        """
        self._env: Mapping[str, str] = env if env is not None else os.environ
        super().__init__(self._env)

        self.__LOCALAPPDATA: Path = self._read_path(
            self._env, EnvironmentVariableKey.LOCALAPPDATA
        )
        self.__USERPROFILE: Path = self._read_path(
            self._env, EnvironmentVariableKey.USERPROFILE
        )
        self.__PIXELPOUCH_LOCATION: Path = self._read_path(
            self._env, EnvironmentVariableKey.PIXELPOUCH_LOCATION
        )

        self.__PIXELPOUCH_ENV: str = self._read_str(
            self._env, EnvironmentVariableKey.PIXELPOUCH_ENV
        )

        self.__PIXELPOUCH_EXECUTION_CONTEXT: str = self._read_str(
            self._env, EnvironmentVariableKey.PIXELPOUCH_EXECUTION_CONTEXT
        )

        # --- debug (always optional attributes) ---
        self.__PIXELPOUCH_DEBUGGER_ENABLE: Optional[bool] = False
        self.__PIXELPOUCH_HOST: str = "0.0.0.0"
        self.__PIXELPOUCH_PORT: int = 0
        if (
            self.PIXELPOUCH_ENV == PixelPouchEnv.DEV
            and self.PIXELPOUCH_EXECUTION_CONTEXT != ExecutionContextEnv.VSCODE
        ):
            self._init_dev()

    def _init_dev(self) -> None:
        self.__PIXELPOUCH_DEBUGGER_ENABLE = self._read_bool_opt(
            self._env, EnvironmentVariableKey.PIXELPOUCH_DEBUGGER_ENABLE
        )
        self.__PIXELPOUCH_HOST = self._read_str(
            self._env, EnvironmentVariableKey.PIXELPOUCH_HOST
        )
        self.__PIXELPOUCH_PORT = self._read_int(
            self._env, EnvironmentVariableKey.PIXELPOUCH_PORT
        )

    @property
    def LOCALAPPDATA(self) -> Path:
        """Returns the path defined by the LOCALAPPDATA environment variable.

        Returns:
            The LOCALAPPDATA directory as a Path object.
        """
        return self.__LOCALAPPDATA

    @property
    def USERPROFILE(self) -> Path:
        """Returns the path defined by the USERPROFILE environment variable.

        Returns:
            The USERPROFILE directory as a Path object.
        """
        return self.__USERPROFILE

    @property
    def PIXELPOUCH_LOCAL_DATA_DIR(self) -> Path:
        """Returns the PixelPouch local data directory.

        This directory is derived by appending ``"PixelPouch"`` to the
        LOCALAPPDATA path.

        Returns:
            The local PixelPouch data directory path.
        """
        return self.LOCALAPPDATA / "PixelPouch"

    @property
    def PIXELPOUCH_LOCATION(self) -> Path:
        """Returns the root installation path of PixelPouch.

        Returns:
            The PixelPouch location as a Path object.
        """
        return self.__PIXELPOUCH_LOCATION

    @property
    def PIXELPOUCH_ENV(self) -> str:
        """Returns the current PixelPouch environment identifier.

        Returns:
            A string representing the active PixelPouch environment.
        """
        return self.__PIXELPOUCH_ENV

    @property
    def PIXELPOUCH_EXECUTION_CONTEXT(self) -> str:
        """Returns the current execution context identifier

        Returns:
            A string representing the active execution context.
        """
        return self.__PIXELPOUCH_EXECUTION_CONTEXT

    # -------------------------
    # properties (debug)
    # -------------------------

    @property
    def PIXELPOUCH_DEBUGGER_ENABLE(self) -> Optional[bool]:
        """Returns whether the PixelPouch debugger is enabled.

        Returns:
            ``True`` or ``False`` if explicitly configured, otherwise ``None``.
        """
        return self.__PIXELPOUCH_DEBUGGER_ENABLE

    @property
    def PIXELPOUCH_HOST(self) -> str:
        """Returns the configured host name for PixelPouch services.

        Returns:
            The host name as a string.
        """
        return self.__PIXELPOUCH_HOST

    @property
    def PIXELPOUCH_PORT(self) -> int:
        """Returns the configured port number for PixelPouch services.

        Returns:
            The port number as an integer.
        """
        return self.__PIXELPOUCH_PORT
