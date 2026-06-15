from logging.config import dictConfig

from app.core.config.settings import settings
from app.core.logging.logging_formatter import (ColoredAccessFormatter,
                                                ColoredDefaultFormatter)
from app.core.logging.request_id_filter import RequestIDFilter


def setup_logging(handler_log_level: str = "DEBUG", root_log_level: str = "INFO", uvicorn_log_level: str = "INFO") -> None:

    """

    Configure centralized application logging for console output only.
    
    This function sets up a centralized logger configuration using Python's built-in logging module. 
    It configures all loggers to write to stdout and uses a consistent format across the app.

    
    Parameters
    ----------
    handler_log_level : str
        Logging level for the default handler as a string. The default value is `"DEBUG"`.
            The options are:
                `"DEBUG"`
                    Detailed diagnostic information.
                `"INFO"`
                    General operational messages confirming normal behavior.
                `"WARNING"`
                    Alerts about unexpected events that don't stop the program.
                `"ERROR"`
                    Serious issues that prevent a function or module from working correctly.
                `"CRITICAL"`
                    Severe errors indicating the program may be unable to continue running.

    root_log_level : str
        Logging level as a string. The default value is `"INFO"`.
            The options are:
                `"DEBUG"`
                    Detailed diagnostic information.
                `"INFO"`
                    General operational messages confirming normal behavior.
                `"WARNING"`
                    Alerts about unexpected events that don't stop the program.
                `"ERROR"`
                    Serious issues that prevent a function or module from working correctly.
                `"CRITICAL"`
                    Severe errors indicating the program may be unable to continue running.

    uvicorn_log_level : str
        Logging level for Uvicorn as a string. The default value is `"INFO"`.
            The options are:
                `"DEBUG"`
                    Detailed diagnostic information.
                `"INFO"`
                    General operational messages confirming normal behavior.
                `"WARNING"`
                    Alerts about unexpected events that don't stop the program.
                `"ERROR"`
                    Serious issues that prevent a function or module from working correctly.
                `"CRITICAL"`
                    Severe errors indicating the program may be unable to continue running.

        
    Returns
    -------
    None.

    """

    if not isinstance(handler_log_level, str):
        raise TypeError(f"handler_log_level must be a string. Received: {handler_log_level} with type {type(handler_log_level)}")
    if not isinstance(root_log_level, str):
        raise TypeError(f"root_log_level must be a string. Received: {root_log_level} with type {type(root_log_level)}")
    if not isinstance(uvicorn_log_level, str):
        raise TypeError(f"uvicorn_log_level must be a string. Received: {uvicorn_log_level} with type {type(uvicorn_log_level)}")

    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if handler_log_level not in valid_levels:
        raise ValueError(f"Invalid handler_log_level: {handler_log_level}. Must be one of: {', '.join(valid_levels)}")
    if root_log_level not in valid_levels:
        raise ValueError(f"Invalid root_log_level: {root_log_level}. Must be one of: {', '.join(valid_levels)}")
    if uvicorn_log_level not in valid_levels:
        raise ValueError(f"Invalid uvicorn_log_level: {uvicorn_log_level}. Must be one of: {', '.join(valid_levels)}")


    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": ColoredDefaultFormatter,
                "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            },
            "access": {
                "()": ColoredAccessFormatter,
                "format": "%(asctime)s - %(levelname)s - %(name)s - [request-id=%(request_id)s] - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": handler_log_level,
                "stream": "ext://sys.stdout",
            },
            "access": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "level": uvicorn_log_level,
                "stream": "ext://sys.stdout",
            },
        },
        "filters": {
            "request_id_filter": {
                "()": RequestIDFilter
            }
        },
        "root": {
            "handlers": ["default"],
            "level": root_log_level,
        },
        "loggers": {
            # This silences Uvicorn's own access logger completely.
            "uvicorn.access": {
                "handlers": [],
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": uvicorn_log_level,
                "propagate": False,
            },
            # This logger is for custom AccessLogMiddleware.
            f"{settings.LOGGER_NAME}.access": {
                "handlers": ["access"],
                "level": uvicorn_log_level,
                "propagate": False,
                "filters": ["request_id_filter"],
            },
        },
    }


    dictConfig(logging_config)
