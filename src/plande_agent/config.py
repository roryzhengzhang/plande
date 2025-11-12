"""Centralised application configuration."""

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime configuration for the agent framework."""

    model_name: str = Field(default="gpt-4o", description="Default planning LLM.")
    embedding_model: str = Field(
        default="text-embedding-3-small", description="Embedding model for tool retrieval."
    )
    max_replan_attempts: int = Field(
        default=2, description="How many times the supervisor will attempt replanning."
    )
    plan_size_limit: int = Field(
        default=15, description="Maximum number of steps returned by the planner."
    )
