"""Supervisor handles execution monitoring and replanning."""

from __future__ import annotations

from typing import Iterable, List, Protocol

from .config import Settings
from .models import ExecutionPlan, Scratchpad, ToolCallResult


class PlannerProtocol(Protocol):
    def build_plan(self, task: str, manifests: Iterable) -> ExecutionPlan:
        ...


class Supervisor:
    """Coordinates execution attempts and triggers replanning when required."""

    def __init__(self, planner: PlannerProtocol, settings: Settings) -> None:
        self._planner = planner
        self._settings = settings

    def run_with_supervision(
        self,
        task: str,
        manifests: Iterable,
        executor_callable,
    ) -> List[ToolCallResult]:
        scratchpad: Scratchpad = Scratchpad({})
        attempts = 0
        call_history: List[ToolCallResult] = []
        plan = self._planner.build_plan(task, manifests)

        while attempts <= self._settings.max_replan_attempts:
            attempts += 1

            for result in executor_callable(plan):
                call_history.append(result)
                if result.error:
                    break
                scratchpad.root[result.output_variable] = result.result
            else:
                # Completed plan successfully
                return call_history

            if attempts > self._settings.max_replan_attempts:
                return call_history

            plan = self._planner.build_plan(task, manifests)

        return call_history
