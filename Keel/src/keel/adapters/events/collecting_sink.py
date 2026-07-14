from keel.domain.schemas.events import EngineEvent


class CollectingEventSink:

    """

    An event sink accumulating engine events in memory.


    Usage
    -----
    Intended for tests and introspection: run the engine, then assert on the
    ordered event stream instead of parsing log output.
    ```python
    from keel.adapters.events import CollectingEventSink

    sink = CollectingEventSink()
    engine = EngineBuilder().with_event_sink(sink).build()

    await engine.run("calculate 2 + 2")
    print([event.type for event in sink.events])
    ```

    """

    def __init__(self) -> None:

        """

        Constructor for the CollectingEventSink class.


        Parameters
        ----------
        None.


        Returns
        -------
        None.


        Raises
        ------
        None.

        """

        self.events: list[EngineEvent] = []


    async def emit(self, event: EngineEvent) -> None:

        """

        Appends an engine event to the collection.


        Parameters
        ----------
        event : EngineEvent
            The event to collect.


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


        self.events.append(event)
