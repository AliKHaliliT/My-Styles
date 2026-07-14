from keel.core.logging import get_logger
from keel.domain.schemas.events import EngineEvent

logger = get_logger("adapters.events")


class LoggingEventSink:

    """

    An event sink forwarding engine events to the package logger.


    Usage
    -----
    This is the default IEventSink implementation. Because the package logger
    carries a NullHandler, events are silent until the host application
    configures logging: observability without imposing output.
    ```python
    from keel.adapters.events import LoggingEventSink

    sink = LoggingEventSink()
    await sink.emit(engine_event)
    ```

    """

    async def emit(self, event: EngineEvent) -> None:

        """

        Logs an engine event at debug level.


        Parameters
        ----------
        event : EngineEvent
            The event to forward.


        Returns
        -------
        None.


        Raises
        ------
        TypeError
            If `event` is not an EngineEvent.

        """

        if not isinstance(event, EngineEvent):
            raise TypeError(f"event must be an EngineEvent. Received: {event} with type {type(event)}")


        logger.debug(f"[{event.run_id}] {event.type}: {event.payload}")
