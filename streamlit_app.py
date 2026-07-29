"""
EDGR Streamlit demo — same Python core as the FastAPI/React workbench.

Deploy on Streamlit Community Cloud with main file: streamlit_app.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

st.set_page_config(
    page_title="EDGR — Research Pipeline",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

EX_QUERIES = [
    "What is CVE-2021-44228 and how is it exploited?",
    "Which ATT&CK techniques does APT29 commonly use?",
    "How can NIDS detect lateral movement?",
]


@st.cache_resource(show_spinner="Loading EDGR core (KG + vector store)…")
def _load_core() -> dict[str, Any]:
    from app.core.knowledge_graph import kg
    from app.core.vector_store import vector_store
    from app.data.cti_seed import QA_DATASET
    from app.pipeline.service import pipeline_service
    from app.services.ids_cti_app import analyze, app_status

    return {
        "pipeline": pipeline_service,
        "kg": kg,
        "vector_store": vector_store,
        "qa_n": len(QA_DATASET),
        "analyze": analyze,
        "app_status": app_status,
    }


def _t(vi: str, en: str, lang: str) -> str:
    return vi if lang == "vi" else en


def _health_cards(core: dict[str, Any], lang: str) -> None:
    stats = core["kg"].stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(_t("KG nodes", "KG nodes", lang), stats.nodes)
    c2.metric(_t("KG edges", "KG edges", lang), stats.edges)
    c3.metric(_t("Evidence", "Evidence chunks", lang), len(core["vector_store"].chunks))
    c4.metric(_t("QA pairs", "QA pairs", lang), core["qa_n"])


def _pretty_json(obj: Any) -> None:
    st.json(obj)


def _result_summary(payload: dict[str, Any], lang: str) -> None:
    cols = st.columns(4)
    cols[0].metric("elapsed_ms", payload.get("elapsed_ms"))
    cols[1].metric(
        _t("tính toán thật", "real computation", lang),
        "yes" if payload.get("real_computation") else "no",
    )
    cols[2].metric("kind", str(payload.get("computation_kind", "—")))
    cols[3].metric("action", str(payload.get("action", "—")))

    review = payload.get("result_review")
    if isinstance(review, dict) and review:
        with st.expander(_t("Đánh giá kết quả", "Result review", lang), expanded=True):
            _pretty_json(review)

    academic = payload.get("academic")
    if isinstance(academic, dict) and academic:
        with st.expander(_t("Khung học thuật", "Academic block", lang), expanded=False):
            _pretty_json(academic)

    with st.expander(_t("Kết quả đầy đủ", "Full result", lang), expanded=True):
        _pretty_json(payload.get("result", payload))


def page_overview(core: dict[str, Any], lang: str) -> None:
    st.subheader(_t("Tổng quan", "Overview", lang))
    st.markdown(
        _t(
            "UI Streamlit gọi **cùng** core Python (`pipeline_service`, `EDGREngine`) "
            "như API FastAPI / React — không mock.",
            "This Streamlit UI calls the **same** Python core "
            "(`pipeline_service`, `EDGREngine`) as the FastAPI / React app — no mocks.",
            lang,
        )
    )
    _health_cards(core, lang)
    definition = core["pipeline"].definition()
    st.caption(
        _t(
            f"Chủ đề: {definition.get('topic_vi') or definition.get('topic')}",
            f"Topic: {definition.get('topic')}",
            lang,
        )
    )
    steps = definition.get("steps") or []
    rows = []
    for s in steps:
        tasks = s.get("tasks") or []
        rows.append(
            {
                "#": s.get("id"),
                _t("Bước", "Step", lang): s.get("title") if lang == "vi" else s.get("title_en"),
                _t("Số task", "Tasks", lang): len(tasks),
                "score": s.get("assessment_score"),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)


def page_pipeline(core: dict[str, Any], lang: str) -> None:
    st.subheader(_t("Pipeline 16 bước", "16-step pipeline", lang))
    definition = core["pipeline"].definition()
    steps = definition.get("steps") or []
    if not steps:
        st.error("Pipeline definition empty")
        return

    labels = [
        f"{s['id']}. {s.get('title') if lang == 'vi' else s.get('title_en')}"
        for s in steps
    ]
    step_idx = st.selectbox(
        _t("Chọn bước", "Select step", lang),
        options=list(range(len(steps))),
        format_func=lambda i: labels[i],
    )
    step = steps[step_idx]
    st.markdown(
        f"**{_t('Mục tiêu', 'Goal', lang)}:** "
        f"{step.get('goal') if lang == 'vi' else step.get('goal_en')}"
    )

    tasks = step.get("tasks") or []
    task_labels = [
        f"{t['id']} — {t.get('title') if lang == 'vi' else t.get('title_en')}"
        for t in tasks
    ]
    task_idx = st.selectbox(
        _t("Chọn task", "Select task", lang),
        options=list(range(len(tasks))),
        format_func=lambda i: task_labels[i],
    )
    task = tasks[task_idx]

    if step.get("id") == 16:
        st.info(
            _t(
                "Bước 16 nên dùng tab **Live IDS/CTI** (analyze) thay vì task console.",
                "For step 16 prefer the **Live IDS/CTI** tab (analyze) over the console task.",
                lang,
            )
        )

    with st.form("run_task_form"):
        query = st.selectbox(
            _t("Query mẫu (tuỳ task)", "Example query (optional per task)", lang),
            options=EX_QUERIES,
            index=0,
        )
        custom = st.text_input(
            _t("Hoặc nhập query tuỳ chỉnh", "Or custom query", lang),
            value="",
        )
        top_k = st.slider("top_k", 1, 10, 5)
        c1, c2, c3 = st.columns(3)
        enable_temporal = c1.checkbox("temporal", value=True)
        enable_graph = c2.checkbox("graph", value=True)
        enable_trust = c3.checkbox("trust_score", value=True)
        submitted = st.form_submit_button(
            _t("Chạy task", "Run task", lang),
            type="primary",
            use_container_width=True,
        )

    if submitted:
        q = (custom or query).strip()
        params = {
            "query": q,
            "top_k": top_k,
            "enable_temporal": enable_temporal,
            "enable_graph": enable_graph,
            "enable_trust_score": enable_trust,
        }
        heavy = step.get("id") in {9, 10, 11}
        spinner = (
            _t(
                "Đang chạy (bước đánh giá có thể lâu)…",
                "Running (evaluation steps can take a while)…",
                lang,
            )
            if heavy
            else _t("Đang chạy…", "Running…", lang)
        )
        try:
            with st.spinner(spinner):
                payload = core["pipeline"].run_task(step["id"], task["id"], params)
            st.success(
                _t(
                    f"Xong: bước {payload.get('step_id')} / {payload.get('task_id')}",
                    f"Done: step {payload.get('step_id')} / {payload.get('task_id')}",
                    lang,
                )
            )
            _result_summary(payload, lang)
        except Exception as e:  # noqa: BLE001
            st.error(str(e))
            st.exception(e)


def page_analyze(core: dict[str, Any], lang: str) -> None:
    st.subheader(_t("Ứng dụng IDS/CTI (live EDGR)", "Live IDS/CTI console", lang))
    status = core["app_status"]()
    st.caption(status.get("note_vi") if lang == "vi" else status.get("note_en"))
    _health_cards(core, lang)

    with st.form("analyze_form"):
        query = st.selectbox(_t("Query mẫu", "Example query", lang), EX_QUERIES, index=0)
        custom = st.text_area(
            _t("Query tuỳ chỉnh", "Custom query", lang),
            value="",
            height=80,
        )
        top_k = st.slider("top_k", 1, 10, 5, key="analyze_topk")
        c1, c2, c3, c4 = st.columns(4)
        enable_temporal = c1.checkbox("temporal", value=True, key="a_t")
        enable_graph = c2.checkbox("graph", value=True, key="a_g")
        enable_trust = c3.checkbox("trust_score", value=True, key="a_s")
        live_enrich = c4.checkbox("NVD live enrich", value=True, key="a_n")
        submitted = st.form_submit_button(
            _t("Phân tích", "Analyze", lang),
            type="primary",
            use_container_width=True,
        )

    if submitted:
        q = (custom or query).strip()
        try:
            with st.spinner(_t("Đang chạy EDGR…", "Running EDGR…", lang)):
                out = core["analyze"](
                    q,
                    top_k=top_k,
                    enable_temporal=enable_temporal,
                    enable_graph=enable_graph,
                    enable_trust_score=enable_trust,
                    live_enrich=live_enrich,
                )
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("confidence", round(float(out.get("confidence") or 0), 3))
            m2.metric("faithfulness", round(float(out.get("faithfulness") or 0), 3))
            m3.metric("hallucination", round(float(out.get("hallucination_rate") or 0), 3))
            m4.metric("latency_ms", out.get("latency_ms"))

            if out.get("abstained"):
                st.warning(
                    out.get("abstain_reason_vi")
                    if lang == "vi"
                    else out.get("abstain_reason_en")
                )

            st.markdown(f"**{_t('Câu trả lời', 'Answer', lang)}**")
            st.write(out.get("answer") or "—")

            evid = out.get("evidence") or []
            if evid:
                st.markdown(f"**{_t('Bằng chứng', 'Evidence', lang)}** ({len(evid)})")
                for i, e in enumerate(evid[: top_k + 2], 1):
                    if isinstance(e, dict):
                        st.markdown(
                            f"{i}. score=`{e.get('score', e.get('trust_score', '—'))}` — "
                            f"{e.get('text') or e.get('content') or e.get('id') or e}"
                        )
                    else:
                        st.markdown(f"{i}. {e}")

            stages = out.get("stage_summary") or out.get("stages") or []
            if stages:
                with st.expander(_t("Các giai đoạn EDGR", "EDGR stages", lang)):
                    _pretty_json(stages)

            with st.expander(_t("Payload đầy đủ", "Full payload", lang)):
                st.code(json.dumps(out, ensure_ascii=False, indent=2)[:120_000])
        except Exception as e:  # noqa: BLE001
            st.error(str(e))
            st.exception(e)


def main() -> None:
    lang = st.sidebar.radio(
        "Language / Ngôn ngữ",
        options=["vi", "en"],
        format_func=lambda x: "Tiếng Việt" if x == "vi" else "English",
        horizontal=True,
    )
    st.title(_t("EDGR — Pipeline nghiên cứu", "EDGR — Research pipeline", lang))
    st.caption(
        _t(
            "Evidence-Driven Dynamic Graph Retrieval · bản Streamlit (cùng core Python)",
            "Evidence-Driven Dynamic Graph Retrieval · Streamlit wrap (same Python core)",
            lang,
        )
    )

    try:
        core = _load_core()
    except Exception as e:  # noqa: BLE001
        st.error(_t("Không tải được core EDGR", "Failed to load EDGR core", lang))
        st.exception(e)
        return

    with st.sidebar:
        st.markdown("---")
        st.markdown(_t("**Trạng thái store**", "**Store status**", lang))
        stats = core["kg"].stats()
        st.write(
            {
                "kg_nodes": stats.nodes,
                "kg_edges": stats.edges,
                "evidence": len(core["vector_store"].chunks),
                "qa_pairs": core["qa_n"],
            }
        )
        st.markdown("---")
        st.caption(
            _t(
                "React UI: `npm run dev` · API: FastAPI `/docs`",
                "React UI: `npm run dev` · API: FastAPI `/docs`",
                lang,
            )
        )

    tab_ov, tab_pipe, tab_app = st.tabs(
        [
            _t("Tổng quan", "Overview", lang),
            _t("Pipeline", "Pipeline", lang),
            _t("Live IDS/CTI", "Live IDS/CTI", lang),
        ]
    )
    with tab_ov:
        page_overview(core, lang)
    with tab_pipe:
        page_pipeline(core, lang)
    with tab_app:
        page_analyze(core, lang)


main()
