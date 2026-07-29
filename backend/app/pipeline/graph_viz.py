"""Build knowledge-graph visualization payloads from the live KG."""

from __future__ import annotations

from typing import Any, Optional

from app.core.knowledge_graph import kg


def kg_viz(
    *,
    title_vi: str = "Đồ thị tri thức",
    title_en: str = "Knowledge graph",
    center: Optional[list[str]] = None,
    limit: int = 28,
    seed_ids: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Return a frontend-ready knowledge_graph viz block."""
    seeds = set(seed_ids or center or [])
    if center:
        sub = kg.subgraph_payload(center_entities=list(center), limit=limit)
    else:
        sub = kg.subgraph_payload(limit=limit)

    nodes = []
    for n in sub.get("nodes", []):
        nid = n.get("id") or n.get("name")
        if not nid:
            continue
        nodes.append(
            {
                "id": str(nid),
                "label": str(n.get("label") or nid),
                "type": str(n.get("type") or "entity"),
                "seed": str(nid) in seeds,
            }
        )
    edges = []
    for e in sub.get("edges", []):
        src = e.get("source") or e.get("from")
        tgt = e.get("target") or e.get("to")
        if not src or not tgt:
            continue
        edges.append(
            {
                "source": str(src),
                "target": str(tgt),
                "relation": str(e.get("relation") or e.get("type") or "related"),
                "weight": float(e.get("weight", 1.0) or 1.0),
            }
        )
    return {
        "kind": "knowledge_graph",
        "title_vi": title_vi,
        "title_en": title_en,
        "nodes": nodes,
        "edges": edges[:80],
    }


def attach_viz(result: dict[str, Any], viz: dict[str, Any]) -> dict[str, Any]:
    out = dict(result)
    out["viz"] = viz
    return out


# Tabs that should show a live KG figure in the academic panel (design-time).
GRAPH_ACADEMIC_TABS: dict[tuple[int, str | None], tuple[str, str]] = {
    (1, "kg"): ("Đồ thị tri thức mẫu (live KG)", "Sample knowledge graph (live KG)"),
    (1, "graphrag"): (
        "Đồ thị con minh họa GraphRAG (live KG)",
        "Illustrative GraphRAG subgraph (live KG)",
    ),
    (4, None): ("Đồ thị phục vụ EDGR (live KG)", "KG backing EDGR (live KG)"),
    (4, "s1"): ("Đồ thị quanh thực thể truy vấn", "Graph around query entities"),
    (4, "s2"): ("Đồ thị sau mở rộng đa bước", "Graph after multi-hop expansion"),
    (4, "s3"): ("Đồ thị sau lọc thời gian", "Graph after temporal filtering"),
    (4, "full"): ("Đồ thị dùng trong pipeline EDGR", "Graph used in the EDGR pipeline"),
    (5, None): ("Dynamic Knowledge Graph (live)", "Dynamic Knowledge Graph (live)"),
    (5, "sources"): ("KG theo nguồn dữ liệu (mẫu)", "KG by data sources (sample)"),
    (5, "extract"): ("Đồ thị trích xuất entity/quan hệ", "Extracted entity/relation graph"),
    (5, "update"): ("KG sau cập nhật gia tăng (mẫu)", "KG after incremental update (sample)"),
    (5, "store"): ("KG trong lớp lưu trữ (mẫu)", "KG in the storage layer (sample)"),
    (6, "consistency"): (
        "Đồ thị dùng để đo nhất quán",
        "Graph used for consistency scoring",
    ),
    (8, "kg_svc"): ("Dịch vụ KG — đồ thị live", "KG service — live graph"),
}


def academic_graph_viz(step_id: int, task_id: str | None) -> dict[str, Any] | None:
    key = (step_id, task_id)
    titles = GRAPH_ACADEMIC_TABS.get(key)
    if not titles and task_id is None:
        # also try step-level only keys already in map
        titles = GRAPH_ACADEMIC_TABS.get((step_id, None))
    if not titles:
        return None
    title_vi, title_en = titles
    # Prefer a CTI-relevant center when the neighborhood is rich enough
    center = None
    for cand in ("CVE-2021-44228", "T1190", "APT29"):
        if cand in kg.graph:
            center = [cand]
            break
    viz = kg_viz(
        title_vi=title_vi,
        title_en=title_en,
        center=center,
        limit=30,
        seed_ids=center,
    )
    # Fall back to a broader sample if the centered subgraph is too thin to read
    if len(viz.get("nodes") or []) < 8:
        viz = kg_viz(
            title_vi=title_vi,
            title_en=title_en,
            center=None,
            limit=30,
            seed_ids=center,
        )
    return viz
