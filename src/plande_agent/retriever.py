"""Tool retriever using embeddings and vector search."""

from __future__ import annotations

from typing import Iterable, List

from .models import ToolManifest


class ToolRetriever:
    """Retrieves relevant tool manifests for a given query."""

    def __init__(self, manifests: Iterable[ToolManifest]) -> None:
        self._manifests = list(manifests)

    def add_manifest(self, manifest: ToolManifest) -> None:
        self._manifests.append(manifest)

    def retrieve(self, query: str, top_k: int = 10) -> List[ToolManifest]:
        """Return top_k manifests by naive lexical similarity placeholder."""
        normalized_query = query.lower()

        def score(manifest: ToolManifest) -> int:
            haystack = f"{manifest.tool_name} {manifest.description}".lower()
            return sum(1 for token in normalized_query.split() if token in haystack)

        sorted_manifests = sorted(self._manifests, key=score, reverse=True)
        return sorted_manifests[:top_k]
