"""Core data models for planning and execution."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, RootModel


class ToolManifest(BaseModel):
    """Structured description of a callable tool."""

    tool_name: str = Field(..., description="Unique identifier for the tool.")
    description: str = Field(..., description="High-signal summary of the tool's capability.")
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    examples: Optional[List[str]] = Field(
        default=None, description="Optional usage examples for retrieval ranking."
    )
    tags: List[str] = Field(default_factory=list, description="Capability tags for filtering.")


class PlanStep(BaseModel):
    """Single step within an execution plan."""

    step_id: str = Field(..., description="Identifier of the step, must be unique within the plan.")
    tool_name: str = Field(..., description="Name of the tool to invoke.")
    description: str = Field(..., description="Rationale for the step.")
    inputs: Dict[str, Any] = Field(..., description="Input arguments or references.")
    output_variable: str = Field(..., description="Scratchpad key to store the tool response.")
    depends_on: List[str] = Field(
        default_factory=list, description="Optional list of step_ids that must finish first."
    )


class ExecutionPlan(BaseModel):
    """Planner output containing ordered steps and final answer instructions."""

    plan: List[PlanStep] = Field(..., min_length=1, description="Ordered list of plan steps.")
    final_answer_instruction: str = Field(
        ..., description="Guidance for synthesising results at the end."
    )

    def topological_order(self) -> List[PlanStep]:
        """Return steps in topological order, raising ValueError on cycles."""
        graph = {step.step_id: set(step.depends_on) for step in self.plan}
        ordered: List[PlanStep] = []
        resolved = set()
        step_map = {step.step_id: step for step in self.plan}

        while graph:
            ready = [step_id for step_id, deps in graph.items() if deps <= resolved]
            if not ready:
                raise ValueError("Cycle detected in execution plan dependencies.")

            for step_id in ready:
                ordered.append(step_map[step_id])
                resolved.add(step_id)
                graph.pop(step_id)

        return ordered


class ToolCallResult(BaseModel):
    """Result of a single tool invocation."""

    step_id: str
    output_variable: str
    result: Any
    error: Optional[str] = None


class Scratchpad(RootModel[Dict[str, Any]]):
    """Execution scratchpad used for storing intermediate tool results."""

    root: Dict[str, Any]
