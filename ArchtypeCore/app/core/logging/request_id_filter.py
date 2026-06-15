from logging import Filter, LogRecord

from app.core.logging.log_context import request_id_var


class RequestIDFilter(Filter):

    """

    A logging filter that adds the current request ID to each log record.
    This allows the request ID to be included in all logs for easier tracing and debugging.


    Usage
    -----
    ```
    from app.core.logging import RequestIDFilter

    "filters": {
        "request_id_filter": {
            "()": RequestIDFilter
        }
    },
    ```

    """

    def filter(self, record: LogRecord) -> bool:

        """

        Injects the current request ID into the log record.

        
        Parameters
        ----------
        record : LogRecord
            The current log record being emitted.

        
        Returns
        -------
        record_logging_switch : bool
            Always returns True to indicate the record should be logged.

        """

        if not isinstance(record, LogRecord):
            raise TypeError(f"record must be an insatnce of the logging.LogRecord. Received: {record} with type {type(record)}")
        

        record.request_id = request_id_var.get()
        return True
