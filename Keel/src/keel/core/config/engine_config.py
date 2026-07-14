from pydantic import BaseModel, ConfigDict, Field


class EngineConfig(BaseModel):

    """

    Immutable configuration for the engine runtime.


    Usage
    -----
    This model is a plain, frozen value object. As a library, the engine never
    reads environment variables or files at import time; the embedding
    application decides where values come from and passes them in explicitly.
    ```python
    from keel.core.config import EngineConfig

    config = EngineConfig(max_steps=4, step_timeout_seconds=10.0)
    ```

    """

    max_steps: int = Field(default=8, ge=1, le=128, description="Maximum number of loop iterations per run")
    step_timeout_seconds: float | None = Field(default=30.0, gt=0, description="Wall-clock budget for a single tool execution; None disables the timeout")
    halt_on_tool_error: bool = Field(default=False, description="Whether a failing tool aborts the run instead of feeding the error back to the reasoner")
    raise_on_exhaustion: bool = Field(default=False, description="Whether consuming the step budget raises StepLimitExceededError instead of returning an exhausted result")

    model_config = ConfigDict(frozen=True)
