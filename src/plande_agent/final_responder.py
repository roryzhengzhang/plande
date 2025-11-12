"""Final response synthesis component."""

from __future__ import annotations

from typing import Protocol

from .models import ExecutionPlan, Scratchpad


class LLMResponder(Protocol):
    def complete(self, prompt: str) -> str:
        ...


class FinalResponder:
    """Transforms scratchpad data into user-facing answers."""

    def __init__(self, llm: LLMResponder) -> None:
        self._llm = llm

    def respond(self, task: str, plan: ExecutionPlan, scratchpad: Scratchpad) -> str:
        prompt = (
            "You are a helpful assistant.\n"
            f"User task: {task}\n"
            f"Instruction: {plan.final_answer_instruction}\n"
            f"Context: {scratchpad.root}\n"
            "Compose a clear response that summarises the task outcome."
        )
        return self._llm.complete(prompt)
