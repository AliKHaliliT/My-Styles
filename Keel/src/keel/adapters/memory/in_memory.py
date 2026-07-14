from keel.domain.schemas.steps import StepRecord


class InMemoryMemory:

    """
    
    A process-local memory store keeping transcripts in a dictionary.
    
    
    Usage
    -----
    This is the default IMemory implementation: zero dependencies, zero
    persistence. Swapping in Redis, SQLite, or a vector store means writing
    another adapter against the same three methods — the engine never knows.
    ```python
    from keel.adapters.memory import InMemoryMemory
    
    memory = InMemoryMemory()
    await memory.record("run-1", step_record)
    transcript = await memory.recall("run-1")
    await memory.forget("run-1")
    ```
    
    """

    def __init__(self) -> None:

        """
        
        Constructor for the InMemoryMemory class.
        
        
        Parameters
        ----------
        None.
        
        
        Returns
        -------
        None.
        
        """

        self._transcripts: dict[str, list[StepRecord]] = {}


    async def record(self, run_id: str, entry: StepRecord) -> None:

        """
        
        Appends a step record to a run's transcript.
        
        
        Parameters
        ----------
        run_id : str
            The identifier of the run.
        
        entry : StepRecord
            The step record to persist.
        
        
        Returns
        -------
        None.
        
        """

        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError(f"run_id must be a non-empty string. Received: {run_id} with type {type(run_id)}")
        if not isinstance(entry, StepRecord):
            raise TypeError(f"entry must be a StepRecord. Received: {entry} with type {type(entry)}")


        self._transcripts.setdefault(run_id, []).append(entry)


    async def recall(self, run_id: str) -> list[StepRecord]:

        """
        
        Fetches the transcript recorded for a run.
        
        
        Parameters
        ----------
        run_id : str
            The identifier of the run.
        
        
        Returns
        -------
        list[StepRecord]
            The recorded steps, in order; empty if the run is unknown.
        
        """

        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError(f"run_id must be a non-empty string. Received: {run_id} with type {type(run_id)}")


        return list(self._transcripts.get(run_id, []))


    async def forget(self, run_id: str) -> None:

        """
        
        Discards the transcript recorded for a run.
        
        
        Parameters
        ----------
        run_id : str
            The identifier of the run.
        
        
        Returns
        -------
        None.
        
        """

        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError(f"run_id must be a non-empty string. Received: {run_id} with type {type(run_id)}")


        self._transcripts.pop(run_id, None)
