import re

from keel.domain.schemas.actions import Action, Finish, ToolCall
from keel.domain.schemas.runs import RunState
from keel.domain.schemas.tools import ToolSpec

_CALCULATE_PATTERN = re.compile(r"^\s*(?:calculate|compute|eval(?:uate)?)\s+(?P<expression>.+?)\s*$", re.IGNORECASE)
_WORD_COUNT_PATTERN = re.compile(r"^\s*count\s+(?:the\s+)?words\s+in\s+(?P<text>.+?)\s*$", re.IGNORECASE)
_CLOCK_PATTERN = re.compile(r"\b(?:time|date)\b", re.IGNORECASE)


class RuleBasedReasoner:

    """

    A deterministic, fully offline reasoner for the demo domain.


    Usage
    -----
    The reasoner pattern-matches the goal to one of the built-in tools, waits
    for the tool result on the transcript, and then finishes with it. It
    exists to prove the architecture: the engine loop, the trace, and every
    port behave identically whether decisions come from these regexes or from
    a frontier model; swap in another IReasoner and nothing else changes.
    ```python
    from keel.adapters.reasoners.rule_based import RuleBasedReasoner

    reasoner = RuleBasedReasoner()
    action = await reasoner.decide(state, tools)
    ```

    """

    async def decide(self, state: RunState, tools: list[ToolSpec]) -> Action:

        """

        Decides the next action for the given run state.


        Parameters
        ----------
        state : RunState
            The evolving state of the run, including the transcript.

        tools : list[ToolSpec]
            The callable contracts currently registered with the engine.


        Returns
        -------
        Action
            A ToolCall while work remains, otherwise a Finish.


        Raises
        ------
        TypeError
            If `state` is not a RunState, or `tools` is not a list.

        """

        if not isinstance(state, RunState):
            raise TypeError(f"state must be a RunState. Received: {state} with type {type(state)}")
        if not isinstance(tools, list):
            raise TypeError(f"tools must be a list. Received: {tools} with type {type(tools)}")


        available = {tool.name for tool in tools}

        if state.transcript:
            last = state.transcript[-1]
            if last.result is not None and not last.result.is_error:
                return Finish(output=last.result.content, rationale="The requested tool produced a result")
            if last.result is not None and last.result.is_error:
                return Finish(output=f"The run could not be completed: {last.result.content}", rationale="The requested tool reported an error")

        match = _CALCULATE_PATTERN.match(state.goal)
        if match and "calculator" in available:
            return ToolCall(tool_name="calculator", arguments={"expression": match.group("expression")}, rationale="The goal asks for an arithmetic evaluation")

        match = _WORD_COUNT_PATTERN.match(state.goal)
        if match and "word_count" in available:
            return ToolCall(tool_name="word_count", arguments={"text": match.group("text")}, rationale="The goal asks for a word count")

        if _CLOCK_PATTERN.search(state.goal) and "clock" in available:
            return ToolCall(tool_name="clock", arguments={}, rationale="The goal asks about the current time or date")

        return Finish(output=f"No registered tool matches the goal: '{state.goal}'", rationale="The rule set has no pattern for this goal")
