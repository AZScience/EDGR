"""Rich Streamlit renderers mirroring React AcademicPanel / DataViz / ResultView."""

from __future__ import annotations

import json
import math
import re
from typing import Any

import pandas as pd
import streamlit as st

try:
    import plotly.graph_objects as go
except ImportError:  # pragma: no cover
    go = None  # type: ignore

RATIO_FIELD = re.compile(
    r"^(faithfulness|hallucination_rate|confidence|p_at_k|r_at_k|mrr|f1|"
    r"precision|recall|accuracy|score|score_0_1|reliability|freshness|"
    r"graph_consistency|semantic_relevance|ent_hit|prefix_stability|"
    r"delta_faithfulness|delta_hallucination)$",
    re.I,
)
LATEX_HINT = re.compile(r"(\$.*\$|\\frac|\\sum|O\(|\\approx|T\(n\)|=O)")

ACAD_BLOCKS = [
    ("csdl", "CSDL / Schema", "CSDL / Schema", "sci-csdl"),
    ("mo_hinh_toan", "Mô hình toán học", "Mathematical model", "sci-math"),
    ("mo_hinh_thuat_toan", "Mô hình thuật toán", "Algorithm model", "sci-algo"),
    ("mo_hinh_hoat_dong", "Mô hình hoạt động", "Operating model", "sci-ops"),
    ("trich_dan", "Trích dẫn", "Citations", "sci-cite"),
    ("minh_chung", "Minh chứng", "Evidence", "sci-ev"),
    ("nhan_dinh_danh_gia", "Nhận định đánh giá", "Assessment", "sci-assess"),
]

DOC_CSS = """
<style>
.doc-section {
  background: rgba(255,255,255,0.78);
  border: 1px solid rgba(15,28,36,0.10);
  border-radius: 14px;
  padding: 0.85rem 1rem 1rem;
  margin: 0.65rem 0 0.9rem;
  box-shadow: 0 10px 28px rgba(15,28,36,0.05);
}
.doc-section-head h4 {
  margin: 0 0 0.2rem;
  display: flex;
  align-items: center;
  gap: 0.55rem;
  font-family: "Fraunces", Georgia, serif !important;
}
.sci-step-num {
  display: inline-flex;
  width: 1.55rem;
  height: 1.55rem;
  border-radius: 999px;
  align-items: center;
  justify-content: center;
  background: #0d7377;
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  font-family: "Sora", sans-serif !important;
}
.doc-section-sub { margin: 0; color: #3a5160; font-size: 0.86rem; }
.critique-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 0.55rem;
  margin-top: 0.55rem;
}
.critique-card {
  border-radius: 10px;
  padding: 0.55rem 0.7rem;
  font-size: 0.86rem;
  border: 1px solid rgba(15,28,36,0.1);
}
.critique-card.good { background: #ecfdf5; border-color: #6ee7b7; }
.critique-card.warn { background: #fff7ed; border-color: #fdba74; }
.critique-card.improve { background: #eff6ff; border-color: #93c5fd; }
.critique-card ul { margin: 0.35rem 0 0; padding-left: 1.05rem; }
.math-card, .algo-step, .db-table-card {
  background: #f8fbfc;
  border: 1px solid rgba(15,28,36,0.1);
  border-radius: 10px;
  padding: 0.55rem 0.7rem;
  margin: 0.4rem 0;
}
.math-label { font-weight: 600; font-size: 0.88rem; color: #0d7377; }
.chip-row { display:flex; flex-wrap:wrap; gap:0.35rem; margin:0.35rem 0; }
.chip {
  background:#eef5f7; border:1px solid rgba(15,28,36,0.1);
  border-radius:999px; padding:0.2rem 0.55rem; font-size:0.78rem;
}
.banner-wrap img { width:100%; border-radius:0 0 14px 14px; display:block; }
.table-guide {
  background:#f0fdfa; border-left:4px solid #0d7377;
  padding:0.55rem 0.75rem; margin:0.35rem 0 0.55rem; border-radius:0 8px 8px 0;
  font-size:0.86rem; color:#3a5160;
}
.stage-row {
  display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.5rem 0 0.8rem;
}
.stage-pill {
  background:#fff; border:1px solid rgba(15,28,36,0.12);
  border-radius:10px; padding:0.35rem 0.55rem; font-size:0.78rem;
}
.rail-active {
  outline: 2px solid #0d7377;
  border-radius: 8px;
}
</style>
"""


def t(vi: str, en: str, lang: str) -> str:
    return vi if lang == "vi" else en


def pick(obj: dict[str, Any], vi_key: str, en_key: str, lang: str, default: str = "") -> str:
    if lang == "vi":
        return str(obj.get(vi_key) or obj.get(en_key) or default)
    return str(obj.get(en_key) or obj.get(vi_key) or default)


def as_str_list(v: Any) -> list[str]:
    if isinstance(v, list):
        return [str(x) for x in v]
    if isinstance(v, str) and v.strip():
        return [v]
    return []


def format_metric(key: str | None, v: Any) -> str:
    if not isinstance(v, (int, float)) or key is None:
        return ""
    if re.search(r"(percent|cpu_percent|system_.*_percent)$", key, re.I):
        return f"{v:.1f}%" if v % 1 else f"{int(v)}%"
    if RATIO_FIELD.match(key) and abs(float(v)) <= 1.0001:
        return f"{float(v) * 100:.1f}%"
    if re.search(r"(rate|ratio|score)$", key, re.I) and abs(float(v)) <= 1.0001:
        return f"{float(v) * 100:.1f}%"
    return ""


def cell(v: Any, key: str | None = None) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (int, float)):
        pct = format_metric(key, v)
        if pct:
            return pct
        if isinstance(v, int) or float(v).is_integer():
            return str(int(v))
        return f"{float(v):.4f}".rstrip("0").rstrip(".")
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        if all(not isinstance(x, (dict, list)) for x in v):
            return ", ".join(str(x) for x in v)
        return f"[{len(v)}]"
    if isinstance(v, dict):
        if "id" in v:
            return str(v["id"])
        try:
            s = json.dumps(v, ensure_ascii=False)
            return s[:117] + "…" if len(s) > 120 else s
        except TypeError:
            return "[object]"
    return str(v)


def collect_keys(rows: list[dict[str, Any]], max_cols: int = 10) -> list[str]:
    preferred = [
        "id", "method", "variant", "authors", "year", "title", "venue", "apa",
        "doi", "tags", "catalog", "synthetic", "citable", "faithfulness",
        "hallucination_rate", "confidence", "latency_ms", "p_at_k", "mrr",
        "f1", "precision", "recall", "score", "paper_id", "limitation",
        "text", "source", "snippet", "statement", "name", "family", "ready",
        "item", "step", "probe", "label", "value", "key", "index",
    ]
    seen: set[str] = set()
    keys: list[str] = []
    for k in preferred:
        if any(k in r for r in rows) and k not in seen:
            seen.add(k)
            keys.append(k)
    for r in rows[:20]:
        for k in r:
            if k in seen or k in {"apa_parts", "metadata", "stages"}:
                continue
            seen.add(k)
            keys.append(k)
            if len(keys) >= max_cols:
                return keys
    return keys[:max_cols]


def maybe_latex(text: str) -> None:
    raw = (text or "").strip()
    if not raw:
        return
    if LATEX_HINT.search(raw) and len(raw) < 400:
        try:
            st.latex(raw.strip("$").strip())
            return
        except Exception:  # noqa: BLE001
            pass
    st.markdown(raw)


def doc_section(num: int, title: str, subtitle: str | None, body) -> None:
    st.markdown(
        f"""
        <div class="doc-section">
          <div class="doc-section-head">
            <h4><span class="sci-step-num">{num}</span>{title}</h4>
            {f'<p class="doc-section-sub">{subtitle}</p>' if subtitle else ''}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    body()


def render_table(
    rows: list[dict[str, Any]],
    caption: str | None = None,
    guide: dict[str, Any] | None = None,
    lang: str = "vi",
    download_name: str | None = None,
) -> None:
    if not rows:
        st.caption("[]")
        return
    if guide:
        bits = []
        for k in ("explain_vi", "explain_en", "evaluate_vi", "evaluate_en", "verdict_vi", "verdict_en"):
            if guide.get(k):
                bits.append(str(guide[k]))
        text = pick(guide, "explain_vi", "explain_en", lang) or (bits[0] if bits else "")
        if text:
            st.markdown(f'<div class="table-guide">{text}</div>', unsafe_allow_html=True)
    keys = collect_keys(rows, max_cols=12)
    data = [{k: cell(r.get(k), k) for k in keys} for r in rows]
    df = pd.DataFrame(data)
    if caption:
        st.markdown(f"**{caption}** ({len(rows)})")
    st.dataframe(df, use_container_width=True, hide_index=True)
    raw = pd.DataFrame(rows)
    csv = raw.to_csv(index=False).encode("utf-8-sig")
    n = st.session_state.get("_dl_n", 0) + 1
    st.session_state["_dl_n"] = n
    st.download_button(
        t("Tải CSV", "Download CSV", lang),
        data=csv,
        file_name=download_name or f"{(caption or 'table').replace(' ', '_')[:40]}.csv",
        mime="text/csv",
        key=f"dl_csv_{n}_{caption or 't'}_{len(rows)}",
    )


def _critique(data: dict[str, Any], lang: str) -> None:
    pros = as_str_list(data.get("pros_vi" if lang == "vi" else "pros_en") or data.get("pros_vi") or data.get("pros_en"))
    cons = as_str_list(data.get("cons_vi" if lang == "vi" else "cons_en") or data.get("cons_vi") or data.get("cons_en"))
    improve = as_str_list(
        data.get("improve_vi" if lang == "vi" else "improve_en") or data.get("improve_vi") or data.get("improve_en")
    )
    if not (pros or cons or improve):
        return
    cards = []
    if pros:
        cards.append(
            '<div class="critique-card good"><strong>'
            + t("Ưu điểm", "Strengths", lang)
            + "</strong><ul>"
            + "".join(f"<li>{x}</li>" for x in pros[:8])
            + "</ul></div>"
        )
    if cons:
        cards.append(
            '<div class="critique-card warn"><strong>'
            + t("Hạn chế", "Limitations", lang)
            + "</strong><ul>"
            + "".join(f"<li>{x}</li>" for x in cons[:8])
            + "</ul></div>"
        )
    if improve:
        cards.append(
            '<div class="critique-card improve"><strong>'
            + t("Cải tiến", "Improvements", lang)
            + "</strong><ul>"
            + "".join(f"<li>{x}</li>" for x in improve[:8])
            + "</ul></div>"
        )
    st.markdown(f'<div class="critique-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def _render_math_block(data: Any, lang: str) -> None:
    if not isinstance(data, dict):
        st.write(data)
        return
    role = pick(data, "role_vi", "role_en", lang)
    narrative = pick(data, "narrative_vi", "narrative_en", lang)
    if role:
        st.markdown(f"**{t('Vai trò', 'Role', lang)}:** {role}")
    if narrative:
        maybe_latex(narrative)
    formulas = data.get("formulas") if isinstance(data.get("formulas"), list) else []
    for i, f in enumerate(formulas):
        if not isinstance(f, dict):
            continue
        label = pick(f, "label_vi", "label_en", lang, t("Công thức", "Formula", lang))
        st.markdown(f'<div class="math-card"><div class="math-label">{label}</div></div>', unsafe_allow_html=True)
        if f.get("latex"):
            maybe_latex(str(f["latex"]))
        explain = pick(f, "explain_vi", "explain_en", lang)
        if explain:
            st.caption(explain)
        vars_ = f.get("variables") if isinstance(f.get("variables"), list) else []
        if vars_:
            rows = []
            for v in vars_:
                if isinstance(v, dict):
                    rows.append(
                        {
                            "symbol": v.get("symbol"),
                            "meaning": pick(v, "vi", "en", lang),
                            "domain": v.get("domain"),
                        }
                    )
            if rows:
                render_table(rows, t("Biến", "Variables", lang), lang=lang, download_name=f"vars_{i}.csv")
    _critique(data, lang)


def _render_algo_block(data: Any, lang: str) -> None:
    if not isinstance(data, dict):
        st.write(data)
        return
    name = pick(data, "name_vi", "name_en", lang, str(data.get("name") or data.get("algorithm") or "Algorithm"))
    st.markdown(f"**{name}**")
    narrative = pick(data, "narrative_vi", "narrative_en", lang)
    if narrative:
        st.write(narrative)
    if data.get("complexity"):
        st.markdown(f"**{t('Độ phức tạp', 'Complexity', lang)}**")
        maybe_latex(str(data["complexity"]))
    steps = as_str_list(data.get("pseudocode") or data.get("steps") or data.get("algo") or [])
    if steps:
        st.markdown(f"**{t('Các bước', 'Steps', lang)}**")
        for i, s in enumerate(steps, 1):
            clean = re.sub(r"^\d+\.\s*", "", s)
            st.markdown(f'<div class="algo-step"><strong>{i}.</strong> {clean}</div>', unsafe_allow_html=True)
    explains = as_str_list(
        data.get("step_explain_vi" if lang == "vi" else "step_explain_en")
        or data.get("step_explain_vi")
        or data.get("step_explain_en")
    )
    if explains:
        with st.container():
            for e in explains:
                st.caption(f"· {e}")
    _critique(data, lang)


def _render_ops_block(data: Any, lang: str) -> None:
    if not isinstance(data, dict):
        st.write(data)
        return
    narrative = pick(data, "narrative_vi", "narrative_en", lang)
    if narrative:
        st.write(narrative)
    stages = data.get("stages") or data.get("flow") or data.get("steps")
    if isinstance(stages, list) and stages:
        pills = []
        for i, s in enumerate(stages, 1):
            if isinstance(s, dict):
                label = pick(s, "name_vi", "name_en", lang, str(s.get("name") or s.get("id") or i))
            else:
                label = str(s)
            pills.append(f'<span class="stage-pill">{i}. {label}</span>')
        st.markdown(f'<div class="stage-row">{"".join(pills)}</div>', unsafe_allow_html=True)
    io_in = as_str_list(data.get("inputs") or data.get("input") or [])
    io_out = as_str_list(data.get("outputs") or data.get("output") or [])
    if io_in or io_out:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{t('Đầu vào', 'Inputs', lang)}**")
            for x in io_in or ["—"]:
                st.markdown(f"- {x}")
        with c2:
            st.markdown(f"**{t('Đầu ra', 'Outputs', lang)}**")
            for x in io_out or ["—"]:
                st.markdown(f"- {x}")
    _critique(data, lang)


def _render_csdl_block(data: Any, lang: str) -> None:
    if not isinstance(data, dict):
        st.write(data)
        return
    name = pick(data, "name_vi", "name_en", lang, str(data.get("name") or data.get("backend") or "CSDL"))
    st.markdown(f"**{name}**")
    explain = pick(data, "explain_vi", "explain_en", lang)
    role = pick(data, "role_vi", "role_en", lang)
    if explain:
        st.write(explain)
    if role:
        st.caption(f"{t('Vai trò', 'Role', lang)}: {role}")
    tables = as_str_list(
        (data.get("tables_vi") if lang == "vi" else data.get("tables_en"))
        or data.get("tables")
        or data.get("sources")
        or data.get("stores")
        or []
    )
    if tables:
        chips = "".join(f'<span class="chip">▤ {x}</span>' for x in tables)
        st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)


def _render_citations_block(data: Any, lang: str) -> None:
    if isinstance(data, list):
        rows = [x for x in data if isinstance(x, dict)]
        if rows:
            render_table(rows, t("Trích dẫn", "Citations", lang), lang=lang, download_name="citations.csv")
        return
    if not isinstance(data, dict):
        st.write(data)
        return
    items = data.get("items") or data.get("citations") or data.get("refs") or []
    if isinstance(items, list) and items and isinstance(items[0], dict):
        render_table(items, t("Trích dẫn", "Citations", lang), lang=lang, download_name="citations.csv")
    else:
        for x in as_str_list(items):
            st.markdown(f"- {x}")
    note = pick(data, "note_vi", "note_en", lang)
    if note:
        st.caption(note)


def _render_evidence_block(data: Any, lang: str) -> None:
    if isinstance(data, list):
        for i, e in enumerate(data[:20], 1):
            if isinstance(e, dict):
                st.markdown(
                    f"{i}. `{cell(e.get('score', e.get('trust_score')), 'score')}` — "
                    f"{e.get('text') or e.get('content') or e.get('apa') or e.get('id') or e}"
                )
            else:
                st.markdown(f"{i}. {e}")
        return
    if not isinstance(data, dict):
        st.write(data)
        return
    claim = pick(data, "claim_vi", "claim_en", lang)
    if claim:
        st.write(claim)
    items = data.get("items") or data.get("examples") or data.get("rows") or []
    if isinstance(items, list) and items and isinstance(items[0], dict):
        render_table(items, t("Minh chứng", "Evidence", lang), lang=lang, download_name="evidence.csv")
    scalars = data.get("scalars") if isinstance(data.get("scalars"), dict) else {}
    if scalars:
        chips = " ".join(
            f'<span class="chip"><strong>{k}</strong> {cell(v, k)}</span>' for k, v in scalars.items()
        )
        st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)


def _render_assess_block(data: Any, lang: str) -> None:
    if not isinstance(data, dict):
        st.write(data)
        return
    score = data.get("score_0_1")
    if isinstance(score, (int, float)):
        st.metric(t("Điểm thiết kế", "Design score", lang), f"{float(score)*100:.0f}%")
    for key in ("summary_vi", "summary_en", "verdict_vi", "verdict_en", "note_vi", "note_en"):
        if lang == "vi" and key.endswith("_en"):
            continue
        if lang == "en" and key.endswith("_vi"):
            continue
        if data.get(key):
            st.write(data[key])
    criteria = data.get("criteria") or data.get("rubric") or []
    if isinstance(criteria, list) and criteria and isinstance(criteria[0], dict):
        render_table(criteria, t("Tiêu chí", "Criteria", lang), lang=lang, download_name="criteria.csv")


def render_block(block_key: str, data: Any, lang: str) -> None:
    if block_key == "csdl":
        _render_csdl_block(data, lang)
    elif block_key == "mo_hinh_toan":
        _render_math_block(data, lang)
    elif block_key == "mo_hinh_thuat_toan":
        _render_algo_block(data, lang)
    elif block_key == "mo_hinh_hoat_dong":
        _render_ops_block(data, lang)
    elif block_key == "trich_dan":
        _render_citations_block(data, lang)
    elif block_key == "minh_chung":
        _render_evidence_block(data, lang)
    elif block_key == "nhan_dinh_danh_gia":
        _render_assess_block(data, lang)
    else:
        st.json(data)


def _heatmap(title: str, row_labels: list[str], col_labels: list[str], values: list[list[float]], binary: bool = False) -> None:
    st.markdown(f"**{title}**")
    if go is None:
        df = pd.DataFrame(values, index=row_labels[: len(values)], columns=col_labels[: len(values[0]) if values else 0])
        st.dataframe(df, use_container_width=True)
        return
    z = values
    colorscale = [[0, "#f3f7f9"], [1, "#0d7377"]] if binary else "Teal"
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=col_labels,
            y=row_labels,
            colorscale=colorscale,
            hoverongaps=False,
        )
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=min(520, 80 + 18 * max(len(row_labels), 8)))
    st.plotly_chart(fig, use_container_width=True)


def _kg_plotly(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], title: str) -> None:
    if go is None or not nodes:
        render_table(nodes[:40], title)
        render_table(edges[:40], "edges")
        return
    ids = [str(n.get("id") or n.get("label") or i) for i, n in enumerate(nodes)]
    id_set = {i: idx for idx, i in enumerate(ids)}
    n = len(ids)
    # circular layout
    xs, ys = [], []
    for i in range(n):
        ang = 2 * math.pi * i / max(n, 1)
        xs.append(math.cos(ang))
        ys.append(math.sin(ang))
    edge_x, edge_y = [], []
    for e in edges:
        a = str(e.get("source") or e.get("from") or e.get("src") or "")
        b = str(e.get("target") or e.get("to") or e.get("dst") or "")
        if a not in id_set or b not in id_set:
            continue
        i, j = id_set[a], id_set[b]
        edge_x += [xs[i], xs[j], None]
        edge_y += [ys[i], ys[j], None]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1, color="#94a3b8"), hoverinfo="none"))
    labels = [str(n.get("label") or n.get("name") or n.get("id") or "") for n in nodes]
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            text=[(lb[:18] + "…") if len(lb) > 18 else lb for lb in labels],
            textposition="top center",
            marker=dict(size=14, color="#0d7377", line=dict(width=1, color="#085456")),
            hovertext=labels,
            hoverinfo="text",
        )
    )
    fig.update_layout(
        title=title,
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=40, b=10),
        height=420,
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_viz_block(viz: dict[str, Any], lang: str) -> None:
    kind = viz.get("kind")
    title = pick(viz, "title_vi", "title_en", lang)
    caption = pick(viz, "caption_vi", "caption_en", lang)
    if title and kind not in {"coverage_matrix", "knowledge_graph"}:
        st.markdown(f"**{title}**")
    if caption:
        st.caption(caption)

    if kind == "bar_chart":
        bars = viz.get("bars") or []
        if bars:
            labels = [pick(b, "label_vi", "label_en", lang, str(i)) for i, b in enumerate(bars)]
            vals = [float(b.get("value") or 0) for b in bars]
            df = pd.DataFrame({"label": labels, "value": vals}).set_index("label")
            st.bar_chart(df)
        return

    if kind == "line_chart":
        points = viz.get("points") or []
        series = viz.get("series") or []
        if points and series:
            df = pd.DataFrame(points)
            if "x" in df.columns:
                df = df.set_index("x")
            cols = [s["key"] for s in series if isinstance(s, dict) and s.get("key") in df.columns]
            if cols:
                st.line_chart(df[cols])
        return

    if kind == "multi_chart":
        for ch in viz.get("charts") or []:
            if isinstance(ch, dict):
                render_viz_block(ch, lang)
        return

    if kind == "coverage_matrix":
        pair_labels = viz.get("pair_labels") if isinstance(viz.get("pair_labels"), list) else []
        pair_matrix = viz.get("pair_matrix") if isinstance(viz.get("pair_matrix"), list) else []
        if pair_labels and pair_matrix:
            _heatmap(
                t("Ma trận đồng xuất hiện chủ đề (Pair)", "Topic co-occurrence matrix (Pair)", lang),
                [str(x) for x in pair_labels],
                [str(x) for x in pair_labels],
                pair_matrix,
            )
        inc_rows = viz.get("incidence_row_labels") if isinstance(viz.get("incidence_row_labels"), list) else []
        inc_cols = viz.get("incidence_col_labels") if isinstance(viz.get("incidence_col_labels"), list) else []
        inc = viz.get("incidence_matrix") if isinstance(viz.get("incidence_matrix"), list) else []
        if inc_rows and inc_cols and inc:
            _heatmap(
                t("Ma trận incidence paper × topic (0/1)", "Paper × topic incidence matrix (0/1)", lang),
                [str(x) for x in inc_rows][:40],
                [str(x) for x in inc_cols][:24],
                [row[:24] for row in inc[:40]],
                binary=True,
            )
        return

    if kind == "knowledge_graph":
        nodes = [n for n in (viz.get("nodes") or []) if isinstance(n, dict)]
        edges = [e for e in (viz.get("edges") or []) if isinstance(e, dict)]
        _kg_plotly(nodes, edges, title or t("Đồ thị tri thức", "Knowledge graph", lang))
        return

    if kind == "architecture":
        layers = viz.get("layers") or viz.get("nodes") or []
        if isinstance(layers, list) and layers:
            render_table(
                [x if isinstance(x, dict) else {"item": x} for x in layers],
                t("Kiến trúc", "Architecture", lang),
                lang=lang,
            )
        else:
            st.json(viz)
        return

    st.json(viz)


def gather_viz(data: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not isinstance(data, dict):
        return out
    viz = data.get("viz")
    if isinstance(viz, dict):
        if viz.get("kind") == "multi_chart" and isinstance(viz.get("charts"), list):
            out.extend(c for c in viz["charts"] if isinstance(c, dict))
        else:
            out.append(viz)
    charts = data.get("charts")
    if isinstance(charts, list):
        out.extend(c for c in charts if isinstance(c, dict))
    stages = data.get("stage_summary") or data.get("stages")
    if isinstance(stages, list) and stages and all(isinstance(s, dict) for s in stages):
        if any("duration_ms" in s for s in stages):
            out.append(
                {
                    "kind": "bar_chart",
                    "title_vi": "Thời gian các giai đoạn EDGR",
                    "title_en": "EDGR stage timings",
                    "bars": [
                        {
                            "label_vi": s.get("name_vi") or s.get("name") or s.get("stage"),
                            "label_en": s.get("name") or s.get("stage"),
                            "value": float(s.get("duration_ms") or 0),
                        }
                        for s in stages
                        if s.get("duration_ms") is not None
                    ],
                }
            )
    return out


def render_academic(pack: dict[str, Any] | None, lang: str, hide_assess: bool = False) -> None:
    if not pack:
        st.caption(t("Chưa có khung học thuật.", "No academic package.", lang))
        return

    st.markdown(DOC_CSS, unsafe_allow_html=True)
    title = pick(pack, "title", "title_en", lang, pack.get("title", ""))
    summary = pick(pack, "summary_vi", "summary_en", lang)
    blocks = pack.get("blocks") if isinstance(pack.get("blocks"), dict) else {}

    score = None
    assess = blocks.get("nhan_dinh_danh_gia") if isinstance(blocks.get("nhan_dinh_danh_gia"), dict) else None
    if not hide_assess and isinstance(assess, dict) and isinstance(assess.get("score_0_1"), (int, float)):
        score = float(assess["score_0_1"])

    head_cols = st.columns([4, 1] if score is not None else [1])
    with head_cols[0]:
        st.markdown(f"### {t('Khung học thuật', 'Academic framework', lang)}")
        if title:
            st.markdown(f"**{title}**")
        if summary:
            st.write(summary)
    if score is not None:
        with head_cols[1]:
            st.metric(t("Điểm", "Score", lang), f"{score*100:.0f}%")

    seq = pack.get("scientific_sequence") or pack.get("sequence")
    if isinstance(seq, list) and seq:
        labels = []
        for i, item in enumerate(seq, 1):
            if isinstance(item, dict):
                labels.append(pick(item, "title_vi", "title_en", lang, str(item.get("id") or i)))
            else:
                labels.append(str(item))
        st.caption(t("Trình tự khoa học", "Scientific sequence", lang) + ": " + " → ".join(labels[:10]))

    theory = pack.get("theory") if isinstance(pack.get("theory"), dict) else None
    if theory:
        def theory_body() -> None:
            name = pick(theory, "name_vi", "name_en", lang)
            if name and name.strip().lower() != str(title).strip().lower():
                st.markdown(f"**{name}**")
            for vk, ek in (
                ("intro_vi", "intro_en"),
                ("what_vi", "what_en"),
                ("why_vi", "why_en"),
                ("argument_vi", "argument_en"),
                ("frame_vi", "frame_en"),
                ("scope_vi", "scope_en"),
            ):
                text = pick(theory, vk, ek, lang)
                if text:
                    st.write(text)
            ideas = as_str_list(
                theory.get("ideas_vi" if lang == "vi" else "ideas_en")
                or theory.get("ideas_vi")
                or theory.get("ideas_en")
            )
            if ideas:
                st.markdown(f"**{t('Ý tưởng chính', 'Key ideas', lang)}**")
                for x in ideas:
                    st.markdown(f"- {x}")
            if theory.get("refs"):
                st.caption(str(theory["refs"]))

        doc_section(1, t("Cơ sở lý thuyết", "Theoretical basis", lang), None, theory_body)

    purpose = pack.get("purpose") if isinstance(pack.get("purpose"), dict) else None
    if purpose:
        def purpose_body() -> None:
            text = pick(purpose, "vi", "en", lang)
            does = pick(purpose, "does_vi", "does_en", lang)
            if text:
                st.write(text)
            if does:
                st.markdown(f"**{t('Tab này làm gì', 'What this tab does', lang)}:** {does}")

        doc_section(2, t("Mục đích", "Purpose", lang), None, purpose_body)

    # Graph preview before evidence — match AcademicPanel
    preview_viz = pack.get("viz") if isinstance(pack.get("viz"), dict) else None
    start_num = 3
    for offset, (key, title_vi, title_en, _anchor) in enumerate(ACAD_BLOCKS):
        if hide_assess and key == "nhan_dinh_danh_gia":
            continue
        block = blocks.get(key)
        if block is None:
            continue
        if key == "minh_chung" and preview_viz:
            doc_section(
                start_num + offset - (1 if hide_assess and "nhan_dinh_danh_gia" in blocks else 0),
                t("Hình minh họa học thuật", "Academic visualization", lang),
                None,
                lambda v=preview_viz: render_viz_block(v, lang),
            )
            preview_viz = None

        def make_body(b=block, k=key):
            def _body() -> None:
                render_block(k, b, lang)

            return _body

        doc_section(start_num + offset, t(title_vi, title_en, lang), None, make_body())

    if preview_viz:
        doc_section(
            99,
            t("Hình minh họa học thuật", "Academic visualization", lang),
            None,
            lambda: render_viz_block(preview_viz, lang),
        )


def render_result_payload(result: Any, lang: str, review: dict[str, Any] | None = None) -> None:
    """Specialize like React ResultView when possible."""
    if result is None:
        st.caption("—")
        return

    for viz in gather_viz(result if isinstance(result, dict) else {}):
        render_viz_block(viz, lang)

    if not isinstance(result, dict):
        st.write(result)
        return

    impl = result.get("implementation")
    if isinstance(impl, str) and "stub" in impl.lower():
        st.markdown(
            f'<div class="honesty">{t("Baseline stub trên cùng store demo.", "Stub baseline on the same demo store.", lang)}'
            f" · <code>{impl}</code></div>",
            unsafe_allow_html=True,
        )
    if result.get("mode") in {"seed_replay", "seed_inventory"}:
        st.markdown(
            f'<div class="honesty">{t("Seed replay trên corpus demo — không crawl API live.", "Seed replay on demo corpus — not a live API crawl.", lang)}</div>',
            unsafe_allow_html=True,
        )

    # Answer prominence
    answer = result.get("answer") or result.get("trusted_answer")
    if isinstance(answer, str) and answer.strip():
        st.markdown(f"#### {t('Câu trả lời / Trusted Answer', 'Answer / Trusted Answer', lang)}")
        st.success(answer)

    # APA catalog
    catalog = result.get("catalog") or result.get("apa_catalog") or result.get("entries")
    if isinstance(catalog, list) and catalog and isinstance(catalog[0], dict):
        if any("apa" in r or "authors" in r for r in catalog[:3]):
            st.markdown(f"#### {t('Danh mục APA', 'APA catalog', lang)}")
            render_table(catalog, t("Catalog", "Catalog", lang), lang=lang, download_name="apa_catalog.csv")

    # Publication / chapter
    if result.get("kind") in {"publication", "manuscript", "chapter"} or result.get("chapters") or result.get("manuscript"):
        ms = result.get("manuscript") or result.get("body") or result.get("content")
        if isinstance(ms, str):
            st.markdown(f"#### {t('Bản thảo', 'Manuscript', lang)}")
            st.markdown(ms[:20000])
        chapters = result.get("chapters") or result.get("outline")
        if isinstance(chapters, list) and chapters and isinstance(chapters[0], dict):
            render_table(chapters, t("Đề cương chương", "Chapter outline", lang), lang=lang)

    # Metrics row
    metric_keys = [
        "faithfulness", "hallucination_rate", "confidence", "p_at_k", "mrr",
        "f1", "latency_ms", "accuracy",
    ]
    present = [k for k in metric_keys if k in result and isinstance(result[k], (int, float))]
    if present:
        cols = st.columns(min(4, len(present)))
        for i, k in enumerate(present[:4]):
            cols[i].metric(k, cell(result[k], k))

    # Table guides from review
    guides = {}
    if isinstance(review, dict):
        tables = review.get("tables")
        if isinstance(tables, dict):
            guides = tables
        ev = review.get("evidence")
        if isinstance(ev, dict) and isinstance(ev.get("tables"), dict):
            guides = {**guides, **ev["tables"]}

    # Remaining structured tables / nested
    skip = {
        "viz", "charts", "answer", "trusted_answer", "catalog", "apa_catalog", "entries",
        "manuscript", "body", "content", "chapters", "outline", "implementation", "mode",
        "note", "note_vi", "note_en", "policy_steps", "stages", "stage_summary",
        *metric_keys,
    }
    for k, v in result.items():
        if k in skip or v is None:
            continue
        if isinstance(v, list) and v and isinstance(v[0], dict):
            guide = guides.get(k) if isinstance(guides.get(k), dict) else None
            render_table(v, k, guide=guide, lang=lang, download_name=f"{k}.csv")
        elif isinstance(v, (str, int, float, bool)):
            continue
        elif isinstance(v, dict):
            st.markdown(f"**{k}**")
            # flatten simple dicts
            if v and all(isinstance(iv, (str, int, float, bool)) or iv is None for iv in v.values()):
                render_table(
                    [{"key": ik, "value": cell(iv, ik)} for ik, iv in v.items()],
                    None,
                    lang=lang,
                    download_name=f"{k}.csv",
                )
            else:
                st.json(v)
        elif isinstance(v, list):
            st.markdown(f"**{k}**")
            for item in v[:30]:
                st.markdown(f"- {item}")

    # leftover note
    note = pick(result, "note_vi", "note_en", lang) or str(result.get("note") or "")
    if note:
        st.caption(note)
