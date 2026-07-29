"""Lightweight TF-IDF vector store for CTI evidence retrieval."""

from __future__ import annotations

from typing import Any, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.data.cti_seed import EVIDENCE_CHUNKS


class VectorStore:
    def __init__(self) -> None:
        self.chunks: list[dict[str, Any]] = list(EVIDENCE_CHUNKS)
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=8000,
        )
        self.matrix = None
        self._fit()

    def _fit(self) -> None:
        corpus = [c["content"] for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(corpus)

    def add(self, chunk: dict[str, Any]) -> None:
        self.chunks.append(chunk)
        self._fit()

    def search(
        self,
        query: str,
        top_k: int = 8,
        entity_boost: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            return []
        q = self.vectorizer.transform([query])
        sims = cosine_similarity(q, self.matrix).flatten()
        boosts = np.zeros_like(sims)
        entities = entity_boost or []
        ent_upper = {e.upper() for e in entities}
        query_l = query.lower()
        for i, chunk in enumerate(self.chunks):
            ents = set(chunk.get("entities", []))
            overlap = len({e.upper() for e in ents}.intersection(ent_upper))
            if overlap:
                boosts[i] += 0.22 * overlap
            # exact ID / label mentions in query text
            for e in ents:
                if e.lower() in query_l:
                    boosts[i] += 0.45
            # source reliability mild prior
            boosts[i] += 0.03 * float(chunk.get("reliability", 0.7))
        scores = sims + boosts
        idx = np.argsort(scores)[::-1][:top_k]
        results: list[dict[str, Any]] = []
        for i in idx:
            if scores[i] <= 0:
                continue
            item = dict(self.chunks[i])
            item["semantic_score"] = float(sims[i])
            item["score"] = float(scores[i])
            results.append(item)
        return results

    def by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        id_set = set(ids)
        return [c for c in self.chunks if c["id"] in id_set]

    def by_entities(self, entities: list[str], top_k: int = 10) -> list[dict[str, Any]]:
        scored: list[tuple[float, dict[str, Any]]] = []
        ent_set = set(entities)
        for c in self.chunks:
            overlap = len(set(c.get("entities", [])).intersection(ent_set))
            if overlap:
                scored.append((overlap + c.get("reliability", 0.5), c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [dict(c, score=float(s)) for s, c in scored[:top_k]]


vector_store = VectorStore()
