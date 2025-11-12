from plande_agent.executor import PlanExecutor
from plande_agent.models import ExecutionPlan
from plande_agent.tool_registry import ToolRegistry


def test_executor_runs_single_step_plan():
    registry = ToolRegistry()

    def echo(value: str) -> str:
        return value.upper()

    registry.register("echo", echo)

    plan = ExecutionPlan.model_validate(
        {
            "plan": [
                {
                    "step_id": "step-1",
                    "tool_name": "echo",
                    "description": "Uppercase the provided text.",
                    "inputs": {"value": "hello"},
                    "output_variable": "greeting",
                    "depends_on": [],
                }
            ],
            "final_answer_instruction": "Use greeting.",
        }
    )

    executor = PlanExecutor(registry)
    results = list(executor.execute(plan))

    assert len(results) == 1
    assert results[0].result == "HELLO"
