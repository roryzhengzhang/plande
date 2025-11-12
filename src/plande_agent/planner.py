"""Planner component responsible for building structured plans."""

from __future__ import annotations

from typing import Iterable, Protocol

from .config import Settings
from .models import ExecutionPlan, ToolManifest


class LLMClient(Protocol):
    """Subset of an LLM client used by Planner."""

    def complete(self, prompt: str) -> str:
        ...


class Planner:
    """Takes a task description plus tool manifests and returns an execution plan."""

    def __init__(self, llm_client: LLMClient, settings: Settings) -> None:
        self._llm = llm_client
        self._settings = settings

    def build_plan(self, task: str, manifests: Iterable[ToolManifest]) -> ExecutionPlan:
        # Placeholder deterministic planner for scaffolding.
        manifest_list = list(manifests)
        if not manifest_list:
            raise ValueError("Planner requires at least one manifest to build a plan.")

        # For now we emit a single-step plan targeting the first manifest.
        best_manifest = manifest_list[0]
        plan = {
            "plan": [
                {
                    "step_id": "step-1",
                    "tool_name": best_manifest.tool_name,
                    "description": f"Call {best_manifest.tool_name} to address the task.",
                    "inputs": {},
                    "output_variable": "result",
                    "depends_on": [],
                }
            ],
            "final_answer_instruction": "Summarise the information under 'result'.",
        }
        return ExecutionPlan.model_validate(plan)
