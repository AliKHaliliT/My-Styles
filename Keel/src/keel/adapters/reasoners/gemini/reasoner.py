from keel.adapters.reasoners.gemini.domain_to_provider import (
    domain_to_provider_contents, domain_to_provider_tools)
from keel.adapters.reasoners.gemini.provider_to_domain import \
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


class GeminiReasoner:

    """

    An IReasoner adapter delegating decisions to the Gemini API.


    Usage
    -----
    This adapter is the seam where a frontier model plugs into the engine. It
    requires the 'gemini' extra; the SDK is imported lazily so the package
    stays importable without it. Authentication follows the SDK's standard
    resolution (the GEMINI_API_KEY environment variable, or an explicit key
    passed by the embedding application, never read by this package).
    ```python
    from keel import EngineBuilder
    from keel.adapters.reasoners.gemini import GeminiReasoner

    engine = EngineBuilder().with_reasoner(GeminiReasoner()).build()
    ```

    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gemini-2.5-flash",
    ) -> None:

        """

        Constructor for the GeminiReasoner class.


        Parameters
        ----------
        api_key : str | None, optional
            An explicit API key; when None, the SDK resolves credentials from its environment.

        model : str, optional
            The model identifier used for decisions.


        Returns
        -------
        None.


        Raises
        ------
        ValueError
            If `api_key` is not a non-empty string or None, or `model` is not a non-empty string.

        EngineConfigurationError
            If the optional 'gemini' dependency is not installed.

        """

        if api_key is not None and (not isinstance(api_key, str) or not api_key.strip()):
            raise ValueError(f"api_key must be a non-empty string or None. Received: {api_key} with type {type(api_key)}")
        if not isinstance(model, str) or not model.strip():
            raise ValueError(f"model must be a non-empty string. Received: {model} with type {type(model)}")


        try:
            from google import genai
        except ImportError as error:
            raise EngineConfigurationError(
                "The GeminiReasoner requires the optional 'gemini' dependency. "
                "Install it with: pip install keel[gemini]"
            ) from error

        self._client = genai.Client(api_key=api_key) if api_key else genai.Client()
        self.model = model


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
            response = await self._client.aio.models.generate_content(
                model=self.model,
                contents=domain_to_provider_contents(state),
                config={
                    "system_instruction": _SYSTEM_PROMPT,
                    "tools": domain_to_provider_tools(tools),
                },
            )
        except ReasoningError:
            raise
        except Exception as error:
            raise ReasoningError(f"The provider request failed: {error}") from error

        return provider_to_domain_action(response)
