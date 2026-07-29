"""Dynamic Knowledge Graph for CTI entities and relations."""

from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone
from typing import Any, Optional

import networkx as nx

from app.data.cti_seed import EDGES, NODES
from app.models.schemas import EntityType, GraphEdge, GraphNode, KGStats


class DynamicKnowledgeGraph:
    """In-memory dynamic KG with incremental updates (Neo4j-compatible shape)."""

    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.last_updated = datetime.now(timezone.utc).isoformat()
        self.sources = [
            "MITRE ATT&CK",
            "CVE/NVD",
            "CWE/CAPEC",
            "CISA/CERT",
            "Threat Feeds",
            "IDS/NIDS",
        ]
        self._bootstrap()

    def _bootstrap(self) -> None:
        for n in NODES:
            self.add_node(GraphNode(**n))
        for e in EDGES:
            self.add_edge(GraphEdge(**e))

    def add_node(self, node: GraphNode) -> None:
        self.graph.add_node(
            node.id,
            label=node.label,
            type=node.type.value if isinstance(node.type, EntityType) else node.type,
            properties=node.properties,
            timestamp=node.timestamp,
            reliability=node.reliability,
        )
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def add_edge(self, edge: GraphEdge) -> None:
        if edge.source not in self.graph or edge.target not in self.graph:
            return
        self.graph.add_edge(
            edge.source,
            edge.target,
            relation=edge.relation,
            weight=edge.weight,
            timestamp=edge.timestamp,
        )
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def get_node(self, node_id: str) -> Optional[dict[str, Any]]:
        if node_id not in self.graph:
            return None
        data = dict(self.graph.nodes[node_id])
        data["id"] = node_id
        return data

    def extract_entities(self, text: str) -> list[str]:
        text_u = text.upper()
        text_l = text.lower()
        found: list[str] = []

        # Regex-first for canonical CTI IDs
        for m in re.findall(r"CVE-\d{4}-\d{4,}", text_u):
            found.append(m)
        for m in re.findall(r"\bT\d{4}(?:\.\d{3})?\b", text_u):
            found.append(m)
        for m in re.findall(r"\bTA\d{4}\b", text_u):
            found.append(m)
        for m in re.findall(r"\bCWE-\d+\b", text_u):
            found.append(m)

        for node_id, data in self.graph.nodes(data=True):
            label = str(data.get("label", ""))
            if node_id.upper() in text_u or (label and label.lower() in text_l):
                found.append(node_id)

        seen: set[str] = set()
        ordered: list[str] = []
        for e in found:
            key = e.upper()
            # normalize to graph id casing when present
            if e in self.graph:
                key_id = e
            else:
                key_id = next(
                    (nid for nid in self.graph.nodes if nid.upper() == key), e
                )
            if key_id not in seen:
                seen.add(key_id)
                ordered.append(key_id)
        return ordered

    def expand(
        self,
        seed_entities: list[str],
        max_hops: int = 2,
        max_nodes: int = 25,
    ) -> list[dict[str, Any]]:
        """Adaptive multi-step neighborhood expansion."""
        visited: set[str] = set()
        frontier = [e for e in seed_entities if e in self.graph]
        results: list[dict[str, Any]] = []

        for hop in range(max_hops):
            next_frontier: list[str] = []
            for node_id in frontier:
                if node_id in visited:
                    continue
                visited.add(node_id)
                node = self.get_node(node_id)
                if node:
                    results.append({**node, "hop": hop})
                # outgoing + incoming
                neighbors = list(self.graph.successors(node_id)) + list(
                    self.graph.predecessors(node_id)
                )
                for nb in neighbors:
                    if nb not in visited:
                        next_frontier.append(nb)
                if len(results) >= max_nodes:
                    return results
            frontier = next_frontier
            if not frontier:
                break
        return results

    def path_consistency(self, entities: list[str]) -> float:
        """Fraction of entity pairs connected within 2 hops."""
        valid = [e for e in entities if e in self.graph]
        if len(valid) < 2:
            return 0.7 if valid else 0.4
        connected = 0
        pairs = 0
        for i in range(len(valid)):
            for j in range(i + 1, len(valid)):
                pairs += 1
                a, b = valid[i], valid[j]
                try:
                    dist = nx.shortest_path_length(
                        self.graph.to_undirected(), a, b
                    )
                    if dist <= 2:
                        connected += 1
                except nx.NetworkXNoPath:
                    pass
        return connected / pairs if pairs else 0.5

    def temporal_filter(
        self,
        entities: list[str],
        reference_date: Optional[datetime] = None,
        window_days: int = 730,
    ) -> list[str]:
        ref = reference_date or datetime.now(timezone.utc)
        kept: list[str] = []
        for eid in entities:
            node = self.get_node(eid)
            if not node:
                continue
            ts = node.get("timestamp")
            if not ts:
                kept.append(eid)
                continue
            try:
                dt = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
                age = (ref - dt).days
                if age <= window_days:
                    kept.append(eid)
            except ValueError:
                kept.append(eid)
        return kept or entities

    def subgraph_payload(
        self, center_entities: Optional[list[str]] = None, limit: int = 40
    ) -> dict[str, Any]:
        if center_entities:
            expanded = self.expand(center_entities, max_hops=2, max_nodes=limit)
            node_ids = {n["id"] for n in expanded}
        else:
            node_ids = set(list(self.graph.nodes)[:limit])

        nodes = []
        for nid in node_ids:
            n = self.get_node(nid)
            if n:
                nodes.append(n)

        edges = []
        for u, v, data in self.graph.edges(data=True):
            if u in node_ids and v in node_ids:
                edges.append(
                    {
                        "source": u,
                        "target": v,
                        "relation": data.get("relation"),
                        "weight": data.get("weight", 1.0),
                        "timestamp": data.get("timestamp"),
                    }
                )
        return {"nodes": nodes, "edges": edges}

    def stats(self) -> KGStats:
        types = Counter(
            str(data.get("type", "unknown"))
            for _, data in self.graph.nodes(data=True)
        )
        return KGStats(
            nodes=self.graph.number_of_nodes(),
            edges=self.graph.number_of_edges(),
            entity_types=dict(types),
            last_updated=self.last_updated,
            sources=self.sources,
        )

    def incremental_update(
        self, nodes: list[dict[str, Any]], edges: list[dict[str, Any]]
    ) -> dict[str, int]:
        before_n = self.graph.number_of_nodes()
        before_e = self.graph.number_of_edges()
        for n in nodes:
            self.add_node(GraphNode(**n))
        for e in edges:
            self.add_edge(GraphEdge(**e))
        return {
            "nodes_added": self.graph.number_of_nodes() - before_n,
            "edges_added": self.graph.number_of_edges() - before_e,
        }

    def relation_summary(self, entities: list[str]) -> list[str]:
        lines: list[str] = []
        for eid in entities:
            if eid not in self.graph:
                continue
            for _, tgt, data in self.graph.out_edges(eid, data=True):
                lines.append(f"{eid} -[{data.get('relation')}]-> {tgt}")
            for src, _, data in self.graph.in_edges(eid, data=True):
                lines.append(f"{src} -[{data.get('relation')}]-> {eid}")
        # unique
        return list(dict.fromkeys(lines))[:20]


# Singleton used by API
kg = DynamicKnowledgeGraph()
