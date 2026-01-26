"""Logging utilities and helpers for the PixelPouch project.

This module provides a custom logger implementation, a singleton-based logger
factory, structured log record creation, and a decorator for tracing function
and method execution. Logging configuration is loaded from a YAML file and
supports environment variable expansion.
"""
import functools
import inspect
import io
import logging
import logging.config
import os
import sys
import threading
import traceback
import types
from enum import IntEnum
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, ParamSpec, TypeAlias, TypeVar, cast

import debugpy
import yaml

from .environment_variable_key import (
    PixelPouchEnvironmentVariables,
)
from .utility import (
    Singleton,
    extract_environment_variables,
)

PP_ENV = PixelPouchEnvironmentVariables()

_R = TypeVar("_R")
_P = ParamSpec("_P")
_logging_ArgsType: TypeAlias = tuple[object, ...] | Mapping[str, object]
_logging_SysExcInfoType: TypeAlias = tuple[type[BaseException] | BaseException | Optional[types.TracebackType]] | tuple[None, None, None]


class LogLevel(IntEnum):
    """Logging level enumeration mapped to the standard ``logging`` module."""

    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

class PixelPouchLogger(logging.getLoggerClass()):  # type: ignore
    """Custom logger class used throughout the PixelPouch project.

    This class subclasses the current logger class returned by
    ``logging.getLoggerClass()`` instead of directly subclassing
    ``logging.Logger``. This ensures compatibility with any custom logger
    class that may have already been installed via ``logging.setLoggerClass()``
    by other code.

    See also:
        https://docs.python.org/3/library/logging.html#logging.getLoggerClass
    """

    def __init__(self, name: str, level: LogLevel = LogLevel.NOTSET) -> None:
        """Initialize a logger with the given name and log level.

        Args:
            name: Logger name.
            level: Initial logging level.
        """
        super().__init__(name, level)


class PixelPouchLoggerFactory(Singleton):
    """Singleton factory responsible for logger creation and configuration."""

    @classmethod
    def get_logger(cls, name: Optional[str] = None) -> PixelPouchLogger:
        """Return a configured logger for the given name.

        If no name is provided, the caller's module or package name is inferred
        from the call stack.

        Args:
            name: Optional logger name.

        Returns:
            A ``PixelPouchLogger`` instance.
        """
        if name is None:
            frame = inspect.stack()[1]
            caller = inspect.getmodule(frame[0])
            assert caller is not None
            if caller.__package__:
                name = caller.__package__
            else:
                name = caller.__name__

        assert name

        logger = logging.getLogger(name)
        return cast(PixelPouchLogger, logger)

    __lock = threading.Lock()
    __initialized = False

    @classmethod
    def _initialize(cls) -> None:
        """Initialize the logging system from the YAML configuration file.

        This method loads logging configuration from ``log_config.yaml``,
        expands environment variables, ensures required directories exist,
        and applies the configuration using ``logging.config.dictConfig``.
        """
        assert not cls.__initialized

        with cls.__lock:
            assert not cls.__initialized
            config_path = Path(__file__).parent / "data" / "log_config.yaml"

            logging.setLoggerClass(PixelPouchLogger)

            with open(config_path.as_posix(), "rt") as file:
                data: Any= yaml.safe_load(file.read())
            data = extract_environment_variables(data)

            log_path = Path(data["handlers"]["file"]["filename"])
            os.makedirs(log_path.parent, exist_ok=True)

            logging.config.dictConfig(data)

            cls.__initialized = True



def __make_record(
    logger: logging.Logger,
    level: LogLevel,
    frame_info: inspect.FrameInfo | traceback.FrameSummary,
    msg: object,
    args: _logging_ArgsType = {},
    exc_info: _logging_SysExcInfoType | None = None,
    stack_info: bool = False,
    extra: Mapping[str, object] | None = None,
) -> logging.LogRecord:
    """Create a ``LogRecord`` with explicit frame and exception handling.

    This function builds a log record using the provided frame information and
    optionally attaches formatted stack trace data when requested.

    Args:
        logger: Logger used to create the record.
        level: Logging level.
        frame_info: Frame or traceback summary providing source information.
        msg: Log message.
        args: Arguments for message formatting.
        exc_info: Exception information to attach to the record.
        stack_info: Whether to include stack trace information.
        extra: Additional contextual information for the log record.

    Returns:
        A fully populated ``logging.LogRecord`` instance.
    """
    lno = frame_info.lineno
    assert lno is not None

    if isinstance(frame_info, inspect.FrameInfo):
        func = frame_info.function
    elif isinstance(frame_info, traceback.FrameSummary):
        func = frame_info.name

    sinfo = None
    if exc_info:
        if isinstance(exc_info, BaseException):
            tb = exc_info.__traceback__.tb_next
            exc_info = (type(exc_info), exc_info, tb)
            if stack_info:
                sio = io.StringIO()
                sio.write("Stack (most recent call last):\n")

                skip = 0

                src_dir = PP_ENV.PIXELPOUCH_LOCATION.resolve()
                stacks = traceback.extract_stack(tb.tb_frame)
                for fs in stacks:
                    fname = Path(fs.filename).resolve()
                    if fname.is_relative_to(src_dir):
                        break
                    else:
                        skip = skip + 1
                        continue

                limit = len(stacks) - skip

                traceback.print_stack(tb.tb_frame, file=sio, limit=limit)
                sinfo = sio.getvalue()
                if sinfo[-1] == "\n":
                    sinfo = sinfo[:-1]
                sio.close()
        elif not isinstance(exc_info, tuple):
            # exc_info = sys.exc_info()
            debugpy.breakpoint()

    return logger.makeRecord(
        name=logger.name,
        level=level,
        fn=frame_info.filename,
        lno=lno,
        msg=msg,
        args=args,
        exc_info=exc_info,
        func=func,
        extra=extra,
        sinfo=sinfo,
    )


def PixelPouch_trace(
    debug_only: bool = False,
    output_error: bool = True,
    stack_info: bool = False,
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """Decorator factory that traces function entry, exit, and errors.

    The returned decorator logs entry and exit points of the wrapped callable.
    When an exception occurs, an error log is emitted and the exception is
    re-raised.

    Args:
        debug_only: If ``True``, tracing is disabled when Python is not running
            in debug mode.
        output_error: Whether to include exception information in error logs.
        stack_info: Whether to include stack trace information on errors.

    Returns:
        A decorator that wraps a callable with tracing logic.
    """

    def __decorator(caller_func_or_class: Callable[_P, _R]) -> Callable[_P, _R]:
        """Decorator that applies tracing to a callable."""
        frame = inspect.stack()[1]
        caller_module = inspect.getmodule(frame[0])
        if hasattr(caller_module, "__package__"):
            name = getattr(caller_module, "__package__")
        elif hasattr(caller_module, "__name__"):
            name = getattr(caller_module, "__name__")
        else:
            raise RuntimeError("Failed to get caller name.")

        assert name

        logger = PixelPouchLoggerFactory.get_logger(name)

        @functools.wraps(caller_func_or_class)
        def __wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            """Wrapped callable with logging and error handling."""
            if not __debug__ and debug_only:
                ret = caller_func_or_class(*args, **kwargs)
                return ret
            else:
                try:
                    # Log - Enter
                    msg = f"{caller_func_or_class.__name__}() - Enter"
                    record = __make_record(logger, LogLevel.DEBUG, frame, msg)
                    logger.handle(record)

                    ret = caller_func_or_class(*args, **kwargs)

                    # Log - Leave
                    msg = f"{caller_func_or_class.__name__}() - Leave"
                    record = __make_record(logger, LogLevel.DEBUG, frame, msg)
                    logger.handle(record)

                    return ret
                except Exception as ex:
                    _, _, traceback_ = sys.exc_info()
                    frame_ = traceback.extract_tb(traceback_)[1]
                    msg = f"{caller_func_or_class.__name__}() - Leave with Error: {ex}"

                    ex = ex if output_error else None

                    record = __make_record(logger, LogLevel.ERROR, frame_, msg, exc_info=ex, stack_info=stack_info)
                    logger.handle(record)

                    raise

        wrapper = __wrapper

        return wrapper

    return __decorator


PixelPouchLoggerFactory._initialize()
