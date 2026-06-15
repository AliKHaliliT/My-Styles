from logging import Formatter, LogRecord

COLORS = {
    "DEBUG": "\033[36m",       # Cyan
    "INFO": "\033[32m",        # Green
    "WARNING": "\033[33m",     # Yellow
    "ERROR": "\033[31m",       # Red
    "CRITICAL": "\033[1;31m",  # Bold Red
}
RESET = "\033[0m"


class ColoredDefaultFormatter(Formatter):

    """

    A custom formatter that adds ANSI color codes to the log level name.

    
    Usage
    -----
    ```
    from app.core.logging import ColoredDefaultFormatter

    "default": {
        "()": ColoredDefaultFormatter,
        "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    },
    ```
    
    """

    def format(self, record: LogRecord) -> str:

        """

        Ensures the log level is colored for console output.

        
        Parameters
        ----------
        record : LogRecord
            The log record to be formatted.

            
        Returns
        -------
        formatted_log : str
            The formatted log message string.

        """

        if not isinstance(record, LogRecord):
            raise TypeError(f"record must be an instance of the logging.LogRecord. Received: {record} with type {type(record)}")


        level_color = COLORS.get(record.levelname, "")
        original_levelname = record.levelname
        record.levelname = f"{level_color}{original_levelname}{RESET}"
        
        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname


class ColoredAccessFormatter(Formatter):

    """

    A custom formatter that adds colors and ensures every log record has a request ID.

    This formatter prevents errors when the request ID is missing by 
    assigning a default value, and colors the log level name.

    
    Usage
    -----
    ```
    from app.core.logging import ColoredAccessFormatter

    "access": {
        "()": ColoredAccessFormatter,
        "format": "%(asctime)s - %(levelname)s - %(name)s - [request-id=%(request_id)s] - %(message)s",
    },
    ```
    
    """

    def format(self, record: LogRecord) -> str:

        """

        Ensures the log record contains a request_id attribute and colors the level name.

        
        Parameters
        ----------
        record : LogRecord
            The log record to be formatted.

            
        Returns
        -------
        formatted_log : str
            The formatted log message string.

        """

        if not isinstance(record, LogRecord):
            raise TypeError(f"record must be an instance of the logging.LogRecord. Received: {record} with type {type(record)}")


        if not hasattr(record, "request_id"):
            record.request_id = "n/a"

        level_color = COLORS.get(record.levelname, "")
        original_levelname = record.levelname
        record.levelname = f"{level_color}{original_levelname}{RESET}"
        
        try:
            return super().format(record)
        finally:
            record.levelname = original_levelname
