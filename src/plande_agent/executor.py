"""Plan execution engine."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from .models import ExecutionPlan, Scratchpad, ToolCallResult
from .tool_registry import ToolRegistry

REF_PATTERN = re.compile(r"^\$steps\.(?P<step>[^.]+)\.(?P<path>.+)$")


class PlanExecutor:
    """Executes DAG plans using the tool registry."""

    def __init__(self, tool_registry: ToolRegistry) -> None:
        self._registry = tool_registry

    def execute(self, plan: ExecutionPlan) -> Iterable[ToolCallResult]:
        scratchpad: Dict[str, Any] = {}

        for step in plan.topological_order():
            resolved_inputs = self._resolve_inputs(step.inputs, Scratchpad(scratchpad))
            tool_func = self._registry.get(step.tool_name)

            try:
                result = tool_func(**resolved_inputs)
                scratchpad[step.output_variable] = result
                scratchpad[step.step_id] = result
                yield ToolCallResult(
                    step_id=step.step_id,
                    output_variable=step.output_variable,
                    result=result,
                )
            except Exception as exc:  # noqa: BLE001
                yield ToolCallResult(
                    step_id=step.step_id,
                    output_variable=step.output_variable,
                    result=None,
                    error=str(exc),
                )
                break

    def _resolve_inputs(self, inputs: Dict[str, Any], scratchpad: Scratchpad) -> Dict[str, Any]:
        resolved: Dict[str, Any] = {}
        for key, value in inputs.items():
            resolved[key] = self._resolve_value(value, scratchpad)
        return resolved

    def _resolve_value(self, value: Any, scratchpad: Scratchpad) -> Any:
        if isinstance(value, str):
            match = REF_PATTERN.match(value)
            if match:
                step_ref = match.group("step")
                path = match.group("path").split(".")
                data = scratchpad.root.get(step_ref)
                for part in path:
                    if data is None:
                        break
                    if part.endswith("]"):
                        name, index = part[:-1].split("[")
                        if name:
                            data = data[name]
                        data = data[int(index)]
                    else:
                        if isinstance(data, dict):
                            data = data.get(part)
                        else:
                            data = getattr(data, part, None)
                return data
        if isinstance(value, list):
            return [self._resolve_value(item, scratchpad) for item in value]
        if isinstance(value, dict):
            return {k: self._resolve_value(v, scratchpad) for k, v in value.items()}
        return value
