"""Tool registry keeps python callables discoverable by the executor."""

from __future__ import annotations

from typing import Any, Callable, Dict


ToolCallable = Callable[..., Any]


class ToolRegistry:
    """Register and retrieve tool callables by name."""

    def __init__(self) -> None:
        self._registry: Dict[str, ToolCallable] = {}

    def register(self, name: str, func: ToolCallable) -> None:
        if name in self._registry:
            raise ValueError(f"Tool '{name}' is already registered.")
        self._registry[name] = func

    def get(self, name: str) -> ToolCallable:
        try:
            return self._registry[name]
        except KeyError as exc:
            raise KeyError(f"Tool '{name}' not found in registry.") from exc

    def available_tools(self) -> Dict[str, ToolCallable]:
        return dict(self._registry)
