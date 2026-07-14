from keel.adapters.reasoners.anthropic.domain_to_provider import (
    domain_to_provider_messages, domain_to_provider_tools)
from keel.adapters.reasoners.anthropic.provider_to_domain import \
    provider_to_domain_action
from keel.domain.exceptions import EngineConfigurationError, ReasoningError
from keel.domain.schemas.actions import Action
from keel.domain.schemas.runs import RunState
from keel.domain.schemas.tools import ToolSpec

_SYSTEM_PROMPT = (
    "You are the decision layer of a bounded agent engine. "
    "On every turn, either call exactly one of the provided tools to make progress toward the goal, "
    "or reply with plain text to conclude the run with a final answer. "
    "Prefer concluding as soon as the transcript already contains what the goal asks for."
)


class AnthropicReasoner:

    """

    An IReasoner adapter delegating decisions to the Anthropic Messages API.


    Usage
    -----
    This adapter is the seam where a frontier model plugs into the engine. It
    requires the 'anthropic' extra; the SDK is imported lazily so the package
    stays importable without it. Authentication follows the SDK's standard
    resolution (the ANTHROPIC_API_KEY environment variable, or an explicit
    key passed by the embedding application, never read by this package).
    ```python
    from keel import EngineBuilder
    from keel.adapters.reasoners.anthropic import AnthropicReasoner

    engine = EngineBuilder().with_reasoner(AnthropicReasoner()).build()
    ```

    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-opus-4-8",
        max_tokens: int = 16000,
    ) -> None:

        """

        Constructor for the AnthropicReasoner class.


        Parameters
        ----------
        api_key : str | None, optional
            An explicit API key; when None, the SDK resolves credentials from its environment.

        model : str, optional
            The model identifier used for decisions.

        max_tokens : int, optional
            The output token ceiling per decision request.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `api_key` is not a non-empty string or None, `model` is not a non-empty string, or `max_tokens` is not a positive integer.

        EngineConfigurationError
            If the optional 'anthropic' dependency is not installed.

        """

        if api_key is not None and (not isinstance(api_key, str) or not api_key.strip()):
            raise ValueError(f"api_key must be a non-empty string or None. Received: {api_key} with type {type(api_key)}")
        if not isinstance(model, str) or not model.strip():
            raise ValueError(f"model must be a non-empty string. Received: {model} with type {type(model)}")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError(f"max_tokens must be a positive integer. Received: {max_tokens} with type {type(max_tokens)}")


        try:
            from anthropic import AsyncAnthropic
        except ImportError as error:
            raise EngineConfigurationError(
                "The AnthropicReasoner requires the optional 'anthropic' dependency. "
                "Install it with: pip install keel[anthropic]"
            ) from error

        self._client = AsyncAnthropic(api_key=api_key) if api_key else AsyncAnthropic()
        self.model = model
        self.max_tokens = max_tokens


    async def decide(self, state: RunState, tools: list[ToolSpec]) -> Action:

        """

        Requests the next action for the given run state from the provider.


        Parameters
        ----------
        state : RunState
            The evolving state of the run, including the transcript.

        tools : list[ToolSpec]
            The callable contracts currently registered with the engine.


        Returns
        -------
        Action
            The provider's decision, translated into the domain.


        Raises
        ------
        TypeError
            If `state` is not a RunState, or `tools` is not a list.

        ReasoningError
            If the provider request fails or yields no usable decision.

        """

        if not isinstance(state, RunState):
            raise TypeError(f"state must be a RunState. Received: {state} with type {type(state)}")
        if not isinstance(tools, list):
            raise TypeError(f"tools must be a list. Received: {tools} with type {type(tools)}")


        try:
            response = await self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=_SYSTEM_PROMPT,
                thinking={"type": "adaptive"},
                tools=domain_to_provider_tools(tools),
                messages=domain_to_provider_messages(state),
            )
        except ReasoningError:
            raise
        except Exception as error:
            raise ReasoningError(f"The provider request failed: {error}") from error

        return provider_to_domain_action(response)
