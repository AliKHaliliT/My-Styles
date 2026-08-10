"""Make one real Gemini call through the adapter and record it for the replay suite.

Run once, with the key arriving from the environment and never from a file:
GEMINI_API_KEY=... python scripts/record_gemini_fixture.py
The recording lands in tests/fixtures/gemini-decide.json, and from then on the suite
replays it offline, so the adapter's wire behavior stays pinned without a key in CI.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from keel.adapters.reasoners.gemini import GeminiReasoner  # noqa: E402
from keel.domain.schemas.runs import RunState  # noqa: E402
from keel.domain.schemas.tools import ToolSpec  # noqa: E402

FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "gemini-decide.json"


async def main() -> int:
    """Ask the live model for one decision and serialize what came back."""
    if not os.environ.get("GEMINI_API_KEY"):
        print("Set GEMINI_API_KEY in the environment first; it is never read from a file.")
        return 1

    reasoner = GeminiReasoner()
    state = RunState(run_id="fixture", goal="count words in: the quick brown fox", max_steps=4)
    tools = [ToolSpec(
        name="word_count",
        description="Counts the words in the given text.",
        parameters={"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]},
    )]

    response = await reasoner._client.aio.models.generate_content(  # noqa: SLF001
        model=reasoner.model,
        contents=[{"role": "user", "parts": [{"text": state.goal}]}],
        config={
            "system_instruction": "Call exactly one of the provided tools.",
            "tools": [{"function_declarations": [{
                "name": t.name, "description": t.description, "parameters_json_schema": t.parameters,
            } for t in tools]}],
        },
    )

    parts = []
    for part in response.candidates[0].content.parts or []:
        call = getattr(part, "function_call", None)
        if call is not None and getattr(call, "name", None):
            parts.append({"function_call": {"name": call.name, "args": dict(call.args or {})}, "text": None})
        elif getattr(part, "text", None):
            parts.append({"function_call": None, "text": part.text})

    recorded = {"prompt_feedback": None, "candidates": [{"content": {"parts": parts}}]}
    FIXTURE.parent.mkdir(exist_ok=True)
    FIXTURE.write_text(json.dumps(recorded, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {len(parts)} part(s) to {FIXTURE}.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
