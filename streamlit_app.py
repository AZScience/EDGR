"""
EDGR Streamlit entry.

Default: embed the **real React SPA** (pixel-perfect) via iframe of FastAPI `/ui/`.
Fallback: native Streamlit panels (approximate parity only).
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import streamlit_parity as parity

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
PUBLIC = ROOT / "frontend" / "public"
DIST = ROOT / "frontend" / "dist"
API_HOST = "127.0.0.1"
API_PORT = 8016
API_BASE = f"http://{API_HOST}:{API_PORT}"
UI_URL = f"{API_BASE}/ui/"

if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))
ABLATION_STEPS = {4, 6, 8, 9, 11}

st.set_page_config(
    page_title="EDGR — Research Pipeline",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── React-aligned step colors ──────────────────────────────────────────
STEP_COLORS: dict[int, str] = {
    0: "#0F766E",
    1: "#2563EB",
    2: "#EA580C",
    3: "#0D9488",
    4: "#16A34A",
    5: "#7C3AED",
    6: "#DC2626",
    7: "#0891B2",
    8: "#4338CA",
    9: "#D97706",
    10: "#059669",
    11: "#DB2777",
    12: "#475569",
    13: "#0284C7",
    14: "#B45309",
    15: "#CA8A04",
    16: "#0F766E",
}

STEP_OVERVIEW = "__overview__"

SAMPLE_QUERIES = [
    "What is CVE-2021-44228 and how is it exploited?",
    "Which ATT&CK techniques does APT29 commonly use?",
    "How can NIDS detect lateral movement?",
    "Which CVE did Cl0p exploit in MOVEit campaigns?",
    "How does EDGR reduce hallucination in CTI answers?",
]

QUICK_QUERIES = [
    {
        "id": "cve",
        "q": SAMPLE_QUERIES[0],
        "label_vi": "CVE-2021-44228",
        "label_en": "CVE-2021-44228",
    },
    {
        "id": "apt",
        "q": SAMPLE_QUERIES[1],
        "label_vi": "TTP APT29",
        "label_en": "APT29 TTPs",
    },
    {
        "id": "lateral",
        "q": SAMPLE_QUERIES[2],
        "label_vi": "Lateral movement",
        "label_en": "Lateral movement",
    },
    {
        "id": "clop",
        "q": SAMPLE_QUERIES[3],
        "label_vi": "Cl0p / MOVEit",
        "label_en": "Cl0p / MOVEit",
    },
]

TOP_K_CHOICES = [3, 5, 8]
DEFAULT_TOP_K = 5

ACAD_BLOCKS = [
    ("csdl", "CSDL / Schema", "CSDL / Schema"),
    ("mo_hinh_toan", "Mô hình toán", "Math model"),
    ("mo_hinh_thuat_toan", "Mô hình thuật toán", "Algorithm model"),
    ("mo_hinh_hoat_dong", "Mô hình hoạt động", "Operating model"),
    ("trich_dan", "Trích dẫn", "Citations"),
    ("minh_chung", "Minh chứng", "Evidence"),
    ("nhan_dinh_danh_gia", "Nhận định đánh giá", "Assessment"),
]

PHASES = [
    {
        "color": "#2563EB",
        "title_vi": "Nền tảng & thiết kế thuật toán",
        "title_en": "Foundation & algorithm design",
        "range_vi": "Bước 1–6",
        "range_en": "Steps 1–6",
        "items_vi": [
            "Khảo sát RAG, GraphRAG, hallucination, CTI/IDS–NIDS",
            "Phân tích khoảng trống và cơ hội đóng góp",
            "Hình thức hóa bài toán giảm hallucination IDS/CTI",
            "Đề xuất thuật toán EDGR (6 giai đoạn)",
            "Thiết kế Dynamic Knowledge Graph",
            "Mô hình chấm điểm rủi ro ảo giác [0, 1]",
        ],
        "items_en": [
            "Survey RAG, GraphRAG, hallucination, CTI/IDS–NIDS",
            "Analyze research gaps and contribution opportunities",
            "Formalize hallucination mitigation for IDS/CTI",
            "Propose EDGR (6 stages)",
            "Design Dynamic Knowledge Graph",
            "Hallucination risk scoring model [0, 1]",
        ],
    },
    {
        "color": "#0D9488",
        "title_vi": "Triển khai & đánh giá",
        "title_en": "Implementation & evaluation",
        "range_vi": "Bước 7–11",
        "range_en": "Steps 7–11",
        "items_vi": [
            "Dữ liệu MITRE / CVE / CISA / IDS → QA",
            "Kiến trúc E2E: query → EDGR ↔ KG/vector/LLM",
            "Thực nghiệm so sánh vs họ RAG baseline",
            "Đánh giá đa chỉ số (faithfulness, hall, P@k, MRR)",
            "Ablation study thành phần thuật toán",
        ],
        "items_en": [
            "MITRE / CVE / CISA / IDS → QA dataset",
            "E2E architecture: query → EDGR ↔ KG/vector/LLM",
            "Comparative experiments vs RAG baselines",
            "Multi-metric evaluation (faithfulness, hall, P@k, MRR)",
            "Ablation study of algorithm components",
        ],
    },
    {
        "color": "#CA8A04",
        "title_vi": "Phân tích, công bố & ứng dụng",
        "title_en": "Analysis, publication & application",
        "range_vi": "Bước 12–16",
        "range_en": "Steps 12–16",
        "items_vi": [
            "Phân tích độ phức tạp, đúng đắn, scalability",
            "Công bố 4 trục: EDGR, DKG, scoring, evaluation",
            "Biên soạn luận án 8 chương",
            "Bảo vệ luận án",
            "Ứng dụng IDS/CTI console (live EDGR)",
        ],
        "items_en": [
            "Complexity, correctness, scalability analysis",
            "Publish on EDGR, DKG, scoring, evaluation",
            "Dissertation outline (8 chapters)",
            "Thesis defense",
            "IDS/CTI console (live EDGR)",
        ],
    },
]

FLOW_VI = [
    "Ý tưởng",
    "Tài liệu",
    "Nghiên cứu",
    "EDGR",
    "Thực nghiệm",
    "Đánh giá",
    "Công bố",
    "Luận án",
    "Bảo vệ",
]
FLOW_EN = [
    "Idea",
    "Literature",
    "Research",
    "EDGR",
    "Experiment",
    "Evaluation",
    "Publication",
    "Dissertation",
    "Defense",
]

RATIO_FIELD = re.compile(
    r"^(faithfulness|hallucination_rate|confidence|p_at_k|r_at_k|mrr|f1|"
    r"precision|recall|accuracy|score|score_0_1|reliability|freshness|"
    r"graph_consistency|semantic_relevance|ent_hit|prefix_stability|"
    r"delta_faithfulness|delta_hallucination)$",
    re.I,
)
LATEX_HINT = re.compile(r"(\$.*\$|\\frac|\\sum|O\(|\\approx|T\(n\)|=O)")


def _is_streamlit_cloud() -> bool:
    """Detect Streamlit Community Cloud (env vars alone are unreliable)."""
    if os.getenv("STREAMLIT_SHARING_MODE") or os.getenv("STREAMLIT_CLOUD"):
        return True
    # Cloud clones into /mount/src/<repo> and runs as adminuser.
    if Path("/mount/src").is_dir():
        return True
    if os.getenv("USER") == "adminuser" or os.getenv("HOME", "").startswith("/home/adminuser"):
        return True
    # Hostname / URL hints when available.
    host = (os.getenv("HOSTNAME") or os.getenv("STREAMLIT_SERVER_BASE_URL_PATH") or "").lower()
    if "streamlit.app" in host or "streamlitcloud" in host:
        return True
    try:
        headers = getattr(getattr(st, "context", None), "headers", None)
        if headers:
            raw = str(headers.get("host") or headers.get("Host") or "").lower()
            if "streamlit.app" in raw:
                return True
    except Exception:  # noqa: BLE001
        pass
    return False

CUSTOM_CSS = """
<style>
@import url("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500&family=Sora:wght@400;500;600;700&display=swap");

html, body, [class*="css"] {
  font-family: "Sora", sans-serif !important;
}
h1, h2, h3, .edgr-brand {
  font-family: "Fraunces", Georgia, serif !important;
  letter-spacing: -0.02em;
}
.stApp {
  background:
    radial-gradient(1000px 520px at 8% -8%, rgba(13, 115, 119, 0.14), transparent 55%),
    radial-gradient(800px 420px at 92% 0%, rgba(196, 92, 38, 0.09), transparent 50%),
    linear-gradient(180deg, #eef5f7 0%, #f3f7f9 45%, #edf3f5 100%);
}
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a2a30 0%, #071820 100%) !important;
  border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
  color: rgba(244, 250, 251, 0.92) !important;
}
section[data-testid="stSidebar"] .stRadio label,
section[data-testid="stSidebar"] label {
  font-size: 0.86rem !important;
}
.edgr-hero {
  background: linear-gradient(120deg, #071820 0%, #0d7377 55%, #c45c26 140%);
  color: #f4fafb;
  border-radius: 0 0 18px 18px;
  padding: 1.1rem 1.35rem 1.25rem;
  margin: -1rem -1rem 1.25rem -1rem;
  box-shadow: 0 10px 28px rgba(15, 28, 36, 0.18);
}
.edgr-hero .kicker {
  font-size: 0.78rem;
  opacity: 0.85;
  margin: 0 0 0.35rem;
  font-family: "Sora", sans-serif;
}
.edgr-hero h1 {
  margin: 0;
  font-size: 1.65rem;
  color: #fff !important;
}
.edgr-hero .meta {
  margin: 0.45rem 0 0;
  opacity: 0.88;
  font-size: 0.88rem;
}
.step-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.28rem 0.7rem;
  border-radius: 999px;
  border: 1px solid;
  font-size: 0.82rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}
.surface {
  background: rgba(255,255,255,0.72);
  border: 1px solid rgba(15, 28, 36, 0.10);
  border-radius: 14px;
  padding: 0.95rem 1.05rem;
  margin-bottom: 0.85rem;
  box-shadow: 0 10px 28px rgba(15, 28, 36, 0.05);
}
.phase-card header {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.45rem;
  border-bottom: 2px solid var(--phase, #0d7377);
  padding-bottom: 0.35rem;
}
.phase-card ul {
  margin: 0.35rem 0 0;
  padding-left: 1.1rem;
  color: #3a5160;
  font-size: 0.9rem;
}
.flow-line {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  align-items: center;
  font-size: 0.86rem;
  font-weight: 600;
  color: #0d7377;
}
.flow-line i { opacity: 0.45; font-style: normal; margin: 0 0.15rem; }
.muted { color: #3a5160; font-size: 0.9rem; }
.tiny { font-size: 0.8rem; }
.mono { font-family: "IBM Plex Mono", monospace !important; }
.review-block {
  background: #fff;
  border-left: 4px solid #0d7377;
  border-radius: 10px;
  padding: 0.75rem 0.9rem;
  margin: 0.55rem 0;
}
.review-block.sci-verify { border-left-color: #059669; }
.review-block.evidence { border-left-color: #c45c26; }
.stat-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin: 0.4rem 0;
}
.stat-chip {
  background: #eef5f7;
  border: 1px solid rgba(15,28,36,0.1);
  border-radius: 10px;
  padding: 0.35rem 0.55rem;
  min-width: 5.5rem;
}
.stat-chip span { display:block; font-size:0.72rem; color:#3a5160; }
.stat-chip strong { font-size:0.95rem; }
.badge-ok { color: #1f7a4c; font-weight: 700; }
.badge-fail { color: #b33a3a; font-weight: 700; }
.honesty {
  background: #fff7ed;
  border: 1px solid #fdba74;
  border-radius: 10px;
  padding: 0.55rem 0.75rem;
  font-size: 0.84rem;
  color: #9a3412;
  margin: 0.4rem 0 0.7rem;
}
div[data-testid="stMetric"] {
  background: rgba(255,255,255,0.7);
  border: 1px solid rgba(15,28,36,0.08);
  border-radius: 12px;
  padding: 0.45rem 0.65rem;
}
.crumb { color:#3a5160; font-size:0.86rem; margin:0 0 0.55rem; }
.progress-pill {
  display:inline-block; background:#0d737722; color:#085456;
  border:1px solid #0d737755; border-radius:999px;
  padding:0.2rem 0.65rem; font-size:0.78rem; font-weight:600;
}
.step-rail-top {
  background: rgba(255,255,255,0.65);
  border: 1px solid rgba(15,28,36,0.1);
  border-radius: 14px;
  padding: 0.55rem 0.65rem 0.2rem;
  margin-bottom: 0.85rem;
}
.stage-row {
  display:flex; flex-wrap:wrap; gap:0.4rem; margin:0.5rem 0 0.8rem;
}
.stage-pill {
  background:#fff; border:1px solid rgba(15,28,36,0.12);
  border-radius:10px; padding:0.35rem 0.55rem; font-size:0.78rem;
}
</style>
"""


@st.cache_resource(show_spinner="Loading EDGR core (KG + vector store)…")
def _load_core() -> dict[str, Any]:
    from app.core.knowledge_graph import kg
    from app.core.vector_store import vector_store
    from app.data.cti_seed import QA_DATASET
    from app.pipeline.service import pipeline_service
    from app.services import alert_ingest
    from app.services.ids_cti_app import analyze, analyze_alert, app_status

    return {
        "pipeline": pipeline_service,
        "kg": kg,
        "vector_store": vector_store,
        "qa_n": len(QA_DATASET),
        "analyze": analyze,
        "analyze_alert": analyze_alert,
        "app_status": app_status,
        "alert_ingest": alert_ingest,
    }


def _t(vi: str, en: str, lang: str) -> str:
    return vi if lang == "vi" else en


def _pick(obj: dict[str, Any], vi_key: str, en_key: str, lang: str, default: str = "") -> str:
    if lang == "vi":
        return str(obj.get(vi_key) or obj.get(en_key) or default)
    return str(obj.get(en_key) or obj.get(vi_key) or default)


def _init_state() -> None:
    ss = st.session_state
    ss.setdefault("lang", "vi")
    ss.setdefault("ui_mode", "native" if _is_streamlit_cloud() else "react")  # react | native
    # Cloud cannot expose localhost FastAPI to the browser — always force native.
    if _is_streamlit_cloud():
        ss.ui_mode = "native"
    ss.setdefault("step_id", 0)
    ss.setdefault("task_id", STEP_OVERVIEW)
    ss.setdefault("result_cache", {})
    ss.setdefault("last_payload", None)
    ss.setdefault("ids_result", None)
    ss.setdefault("ids_mode", "alert")
    ss.setdefault("selected_alert_id", None)
    ss.setdefault("_backend_started", False)


def _api_healthy() -> bool:
    try:
        with urllib.request.urlopen(f"{API_BASE}/api/health", timeout=2) as resp:
            return int(getattr(resp, "status", 200) or 200) == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def _ensure_backend() -> bool:
    """Reuse running FastAPI or start one in a daemon thread."""
    if _api_healthy():
        return True
    if st.session_state.get("_backend_started"):
        for _ in range(40):
            if _api_healthy():
                return True
            time.sleep(0.25)
        return _api_healthy()

    def _run() -> None:
        import uvicorn

        uvicorn.run(
            "app.main:app",
            host=API_HOST,
            port=API_PORT,
            reload=False,
            log_level="warning",
        )

    threading.Thread(target=_run, name="edgr-fastapi", daemon=True).start()
    st.session_state._backend_started = True
    for _ in range(60):
        if _api_healthy():
            return True
        time.sleep(0.25)
    return False


def page_react_embed(lang: str) -> None:
    """Fullscreen iframe of the real React SPA (same CSS/layout/behavior)."""
    st.markdown(
        """
        <style>
          [data-testid="stHeader"],
          [data-testid="stToolbar"],
          [data-testid="stDecoration"] { display: none !important; }
          .block-container { padding: 0.4rem 0.6rem 0.2rem !important; max-width: 100% !important; }
          iframe { border: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if not DIST.is_dir() or not (DIST / "index.html").is_file():
        st.error(
            _t(
                "Chưa có bản build React (`frontend/dist`). Chạy: cd frontend && npm run build",
                "React build missing (`frontend/dist`). Run: cd frontend && npm run build",
                lang,
            )
        )
        st.code("cd frontend\nnpm run build", language="bash")
        return

    ok = _ensure_backend()
    if not ok:
        st.error(
            _t(
                f"Không khởi động được API tại {API_BASE}. Hãy chạy backend thủ công.",
                f"Cannot start API at {API_BASE}. Start the backend manually.",
                lang,
            )
        )
        st.code(
            f"cd backend\npython -m uvicorn app.main:app --host {API_HOST} --port {API_PORT}",
            language="bash",
        )
        return

    # Prefer built SPA on FastAPI; also offer live Vite if running
    src = UI_URL
    try:
        with urllib.request.urlopen(UI_URL, timeout=2) as resp:
            if int(getattr(resp, "status", 200) or 200) >= 400:
                src = "http://127.0.0.1:5180/"
    except (urllib.error.URLError, TimeoutError, OSError):
        # Fallback to Vite dev server if SPA mount not ready
        try:
            with urllib.request.urlopen("http://127.0.0.1:5180/", timeout=1):
                src = "http://127.0.0.1:5180/"
        except (urllib.error.URLError, TimeoutError, OSError):
            st.warning(
                _t(
                    "API chạy nhưng /ui/ chưa sẵn sàng — restart backend sau khi npm run build.",
                    "API is up but /ui/ is not ready — restart backend after npm run build.",
                    lang,
                )
            )
            return

    st.caption(
        _t(
            f"Đang nhúng UI React gốc · {src}  (đây là cùng SPA với :5180, không phải mock Streamlit)",
            f"Embedding real React UI · {src}  (same SPA as :5180 — not a Streamlit mock)",
            lang,
        )
    )
    components.iframe(src, height=920, scrolling=True)


def _inject_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def _health_cards(core: dict[str, Any], lang: str) -> None:
    stats = core["kg"].stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("KG nodes", stats.nodes)
    c2.metric("KG edges", stats.edges)
    c3.metric(_t("Evidence", "Evidence chunks", lang), len(core["vector_store"].chunks))
    c4.metric(_t("QA pairs", "QA pairs", lang), core["qa_n"])


def _format_metric(key: str | None, v: Any) -> str:
    if not isinstance(v, (int, float)) or key is None:
        return ""
    if re.search(r"(percent|cpu_percent|system_.*_percent)$", key, re.I):
        return f"{v:.1f}%" if v % 1 else f"{int(v)}%"
    if RATIO_FIELD.match(key) and abs(float(v)) <= 1.0001:
        return f"{float(v) * 100:.1f}%"
    if re.search(r"(rate|ratio|score)$", key, re.I) and abs(float(v)) <= 1.0001:
        return f"{float(v) * 100:.1f}%"
    return ""


def _cell(v: Any, key: str | None = None) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (int, float)):
        pct = _format_metric(key, v)
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


def _collect_keys(rows: list[dict[str, Any]], max_cols: int = 10) -> list[str]:
    preferred = [
        "id", "method", "variant", "authors", "year", "title", "venue", "apa",
        "doi", "tags", "catalog", "synthetic", "citable", "faithfulness",
        "hallucination_rate", "confidence", "latency_ms", "p_at_k", "mrr",
        "f1", "precision", "recall", "score", "paper_id", "limitation",
        "text", "source", "severity", "statement", "name", "family", "ready",
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


def _render_table(rows: list[dict[str, Any]], caption: str | None = None) -> None:
    parity.render_table(rows, caption, lang=st.session_state.get("lang", "vi"))


def _maybe_latex(text: str) -> None:
    parity.maybe_latex(text)


def _render_viz_block(viz: dict[str, Any], lang: str) -> None:
    parity.render_viz_block(viz, lang)


def _gather_viz(data: Any) -> list[dict[str, Any]]:
    return parity.gather_viz(data)

def _render_scientific_verify(verification: dict[str, Any], lang: str) -> None:
    status = verification.get("runtime_status") or "pending"
    status_label = _pick(verification, "runtime_status_vi", "runtime_status_en", lang)
    protocol = _pick(verification, "protocol_vi", "protocol_en", lang)
    st.markdown(
        f'<div class="review-block sci-verify"><strong>'
        f'{_t("Xác minh khoa học", "Scientific verification", lang)}</strong> · '
        f'<code>{status}</code>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if status_label:
        st.write(status_label)
    if protocol:
        st.caption(f"{_t('Giao thức', 'Protocol', lang)}: {protocol}")
    for c in verification.get("checks") or []:
        if not isinstance(c, dict):
            continue
        ok = bool(c.get("ok"))
        mark = "✓" if ok else "✗"
        cls = "badge-ok" if ok else "badge-fail"
        title = _pick(c, "title_vi", "title_en", lang, c.get("id", ""))
        detail = _pick(c, "detail_vi", "detail_en", lang)
        st.markdown(
            f'<span class="{cls}">{mark}</span> **{title}** — {detail}',
            unsafe_allow_html=True,
        )
    expert = verification.get("expert")
    if isinstance(expert, dict):
        st.caption(
            _pick(expert, "status_vi", "status_en", lang)
            + (
                f" · κ={expert['kappa']:.2f}"
                if isinstance(expert.get("kappa"), (int, float))
                else ""
            )
        )


def _render_result_review(review: dict[str, Any], lang: str) -> None:
    if not review:
        return
    st.subheader(_t("Đánh giá kết quả", "Result review", lang))
    ver = review.get("scientific_verification")
    if isinstance(ver, dict):
        _render_scientific_verify(ver, lang)

    bullets = review.get("bullets_vi") if lang == "vi" else review.get("bullets_en")
    if not bullets:
        bullets = review.get("bullets_vi") or review.get("bullets_en") or []
    explain = _pick(review, "explain_vi", "explain_en", lang)
    how = _pick(review, "how_to_read_vi", "how_to_read_en", lang)

    st.markdown('<div class="review-block">', unsafe_allow_html=True)
    st.markdown(f"**{_t('Giải thích', 'Explanation', lang)}**")
    if bullets:
        for b in bullets:
            st.markdown(f"- {b}")
    elif explain:
        st.write(explain)
    st.markdown("</div>", unsafe_allow_html=True)

    ev = review.get("evidence")
    if isinstance(ev, dict):
        claim = _pick(ev, "claim_vi", "claim_en", lang)
        scalars = ev.get("scalars") if isinstance(ev.get("scalars"), dict) else {}
        if claim or scalars:
            st.markdown('<div class="review-block evidence">', unsafe_allow_html=True)
            st.markdown(f"**{_t('Minh chứng', 'Evidence', lang)}**")
            if claim:
                st.write(claim)
            if scalars:
                chips = " ".join(
                    f'<span class="stat-chip"><span>{k}</span><strong>{_cell(v, k)}</strong></span>'
                    for k, v in scalars.items()
                )
                st.markdown(f'<div class="stat-row">{chips}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    if how:
        st.caption(f"{_t('Cách đọc', 'How to read', lang)}: {how}")

    assessment = review.get("assessment")
    if isinstance(assessment, dict) and assessment:
        with st.expander(_t("Đánh giá runtime", "Runtime assessment", lang)):
            _render_generic_value(assessment, lang, depth=1)


def _render_generic_value(data: Any, lang: str, depth: int = 0) -> None:
    if data is None:
        st.caption("—")
        return
    if isinstance(data, (str, int, float, bool)):
        if isinstance(data, str) and LATEX_HINT.search(data):
            _maybe_latex(data)
        else:
            st.write(data)
        return
    if isinstance(data, list):
        if not data:
            st.caption("[]")
            return
        if isinstance(data[0], dict):
            _render_table(data, None)
            return
        if all(not isinstance(x, (dict, list)) for x in data):
            _render_table(
                [{"index": i + 1, "value": x} for i, x in enumerate(data)],
                None,
            )
            return
        for i, item in enumerate(data[:30]):
            if depth == 0:
                with st.expander(f"[{i}]"):
                    _render_generic_value(item, lang, depth + 1)
            else:
                st.markdown(f"**[{i}]**")
                _render_generic_value(item, lang, depth + 1)
        return

    if isinstance(data, dict):
        # Honesty badges
        impl = data.get("implementation")
        if isinstance(impl, str) and "stub" in impl.lower():
            st.markdown(
                f'<div class="honesty">{_t("Baseline stub trên cùng store demo.", "Stub baseline on the same demo store.", lang)}'
                f" · <code>{impl}</code></div>",
                unsafe_allow_html=True,
            )
        note = _pick(data, "note_vi", "note_en", lang) or str(data.get("note") or "")
        if data.get("mode") in {"seed_replay", "seed_inventory"}:
            st.markdown(
                f'<div class="honesty">{_t("Seed replay trên corpus demo — không crawl API live.", "Seed replay on demo corpus — not a live API crawl.", lang)}</div>',
                unsafe_allow_html=True,
            )
        if note and depth == 0:
            st.caption(note)

        for viz in _gather_viz(data):
            _render_viz_block(viz, lang)

        scalars: list[tuple[str, Any]] = []
        tables: list[tuple[str, list[dict[str, Any]]]] = []
        nested: list[tuple[str, Any]] = []
        skip = {
            "viz", "charts", "note", "note_vi", "note_en", "implementation",
            "policy_steps", "mode", "stages",
        }
        for k, v in data.items():
            if k in skip or v is None:
                continue
            if isinstance(v, (str, int, float, bool)):
                scalars.append((k, v))
            elif (
                isinstance(v, list)
                and v
                and isinstance(v[0], dict)
            ):
                tables.append((k, v))
            elif isinstance(v, list) and all(not isinstance(x, (dict, list)) for x in v):
                tables.append((k, [{"index": i + 1, "value": x} for i, x in enumerate(v)]))
            elif isinstance(v, dict):
                inner = v
                if inner and all(
                    isinstance(iv, (str, int, float, bool)) or iv is None
                    for iv in inner.values()
                ):
                    tables.append(
                        (k, [{"key": ik, "value": iv} for ik, iv in inner.items()])
                    )
                else:
                    nested.append((k, v))
            else:
                nested.append((k, v))

        if scalars:
            _render_table(
                [{"field": k, "value": _cell(v, k)} for k, v in scalars],
                _t("Chỉ số", "Scalars", lang),
            )
        for key, rows in tables:
            _render_table(rows, key)
        for key, val in nested:
            # Streamlit forbids nested expanders — only top-level uses them.
            if depth == 0:
                with st.expander(key, expanded=len(nested) <= 3):
                    _render_generic_value(val, lang, depth + 1)
            else:
                st.markdown(f"**{key}**")
                _render_generic_value(val, lang, depth + 1)


def _render_academic(pack: dict[str, Any] | None, lang: str, hide_assess: bool = False) -> None:
    parity.render_academic(pack, lang, hide_assess=hide_assess)


def _hero(lang: str, health_line: str, done: int = 0, total: int = 16) -> None:
    banner = PUBLIC / "edgr-topic-banner.png"
    if banner.is_file():
        st.image(str(banner), use_container_width=True)
    st.markdown(
        f"""
        <div class="edgr-hero">
          <p class="kicker">{_t(
            "Truy hồi đồ thị động dựa trên bằng chứng · IDS / CTI",
            "Evidence-driven dynamic graph retrieval · IDS / CTI",
            lang,
          )}</p>
          <h1 class="edgr-brand">EDGR — {_t("Pipeline nghiên cứu A→Z", "Research pipeline A→Z", lang)}</h1>
          <p class="meta">{health_line}
            · <span class="progress-pill">{done}/{total} {_t('đã chạy', 'done', lang)}</span>
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _step_badge(step_id: int, title: str) -> None:
    color = STEP_COLORS.get(step_id, "#0d7377")
    st.markdown(
        f'<div class="step-chip" style="color:{color};border-color:{color}55;background:{color}14">'
        f"◈ {_t(f'Bước {step_id}', f'Step {step_id}', st.session_state.lang)}. {title}"
        f"</div>",
        unsafe_allow_html=True,
    )


def page_overview(core: dict[str, Any], lang: str) -> None:
    definition = core["pipeline"].definition()
    topic = _pick(definition, "topic_vi", "topic", lang, definition.get("topic", ""))
    _step_badge(0, _t("Quy trình nghiên cứu", "Research process", lang))
    st.markdown(f'<div class="surface"><p class="muted">{topic}</p></div>', unsafe_allow_html=True)

    process = PUBLIC / ("quy-trinh-a-z-en.png" if lang == "en" else "quy-trinh-a-z.png")
    if process.is_file():
        st.image(str(process), use_container_width=True)

    st.markdown(f"### {_t('Giải thích tổng quan', 'Overview explanation', lang)}")
    st.write(
        _t(
            "Sơ đồ trình bày khung nghiên cứu tiến sĩ theo ba giai đoạn: "
            "(i) nền tảng lý thuyết và thiết kế thuật toán; "
            "(ii) triển khai hệ thống cùng thực nghiệm–đánh giá; "
            "(iii) phân tích thuật toán, công bố khoa học và chuyển giao kết quả. "
            "Trục đóng góp là EDGR (Evidence-Driven Dynamic Graph Retrieval).",
            "The diagram presents the PhD research frame in three phases: "
            "(i) theoretical foundation and algorithm design; "
            "(ii) system implementation with experiments–evaluation; "
            "(iii) algorithm analysis, scientific publication and transfer. "
            "The contribution axis is EDGR (Evidence-Driven Dynamic Graph Retrieval).",
            lang,
        )
    )
    st.write(
        _t(
            "Đóng góp khoa học tập trung ở các bước 4–6: EDGR tích hợp mở rộng đồ thị thích ứng, "
            "lọc thời gian, xếp hạng bằng chứng và cổng tin cậy trước Trusted Answer cho IDS/CTI.",
            "Scientific contribution centers on steps 4–6: EDGR integrates adaptive graph expansion, "
            "temporal filtering, evidence ranking and a trust gate before Trusted Answers for IDS/CTI.",
            lang,
        )
    )

    cols = st.columns(3)
    for col, phase in zip(cols, PHASES):
        with col:
            items = phase["items_vi"] if lang == "vi" else phase["items_en"]
            lis = "".join(f"<li>{x}</li>" for x in items)
            st.markdown(
                f"""
                <div class="surface phase-card" style="--phase:{phase['color']}">
                  <header>
                    <strong>{phase['title_vi' if lang=='vi' else 'title_en']}</strong>
                    <span>{phase['range_vi' if lang=='vi' else 'range_en']}</span>
                  </header>
                  <ul>{lis}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    flow = FLOW_VI if lang == "vi" else FLOW_EN
    flow_html = " <i>→</i> ".join(f"<span>{n}</span>" for n in flow)
    st.markdown(
        f'<div class="surface"><h4>{_t("A→Z: Từ ý tưởng đến đóng góp khoa học", "A→Z: From idea to scientific contribution", lang)}</h4>'
        f'<div class="flow-line">{flow_html}</div></div>',
        unsafe_allow_html=True,
    )

    _health_cards(core, lang)

    st.markdown(f"### {_t('Đi tới từng bước nghiên cứu', 'Jump to research steps', lang)}")
    steps = definition.get("steps") or []
    grid = st.columns(4)
    for i, s in enumerate(steps):
        sid = int(s["id"])
        color = STEP_COLORS.get(sid, "#0d7377")
        label = s.get("title") if lang == "vi" else s.get("title_en")
        with grid[i % 4]:
            if st.button(
                f"{sid}. {label}",
                key=f"jump_{sid}",
                use_container_width=True,
            ):
                st.session_state.step_id = sid
                st.session_state.task_id = STEP_OVERVIEW
                st.session_state.last_payload = None
                st.rerun()
            st.markdown(
                f'<div style="height:4px;border-radius:4px;background:{color};margin:-0.35rem 0 0.65rem"></div>',
                unsafe_allow_html=True,
            )

    rows = []
    for s in steps:
        rows.append(
            {
                "#": s.get("id"),
                _t("Bước", "Step", lang): s.get("title") if lang == "vi" else s.get("title_en"),
                _t("Số task", "Tasks", lang): len(s.get("tasks") or []),
                "score": s.get("assessment_score"),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)


def page_step(core: dict[str, Any], lang: str, step_id: int) -> None:
    definition = core["pipeline"].definition()
    steps = definition.get("steps") or []
    step = next((s for s in steps if s.get("id") == step_id), None)
    if not step:
        st.error(f"Unknown step {step_id}")
        return

    title = step.get("title") if lang == "vi" else step.get("title_en")
    goal = step.get("goal") if lang == "vi" else step.get("goal_en")
    st.markdown(
        f'<p class="crumb">{_t("Tổng quan", "Overview", lang)} → '
        f'{_t(f"Bước {step_id}", f"Step {step_id}", lang)} · {title}</p>',
        unsafe_allow_html=True,
    )
    _step_badge(step_id, str(title))
    st.write(goal or "")
    st.caption(
        _t(
            "Trình tự khoa học: Tổng quan bước → từng công việc con (mô hình → chạy → minh chứng).",
            "Scientific sequence: step overview → child tasks (model → run → evidence).",
            lang,
        )
    )

    tasks = step.get("tasks") or []
    task_options = [STEP_OVERVIEW] + [t["id"] for t in tasks]
    labels = {
        STEP_OVERVIEW: _t("▸ Tổng quan bước", "▸ Step overview", lang),
    }
    for i, t in enumerate(tasks):
        tid = t["id"]
        done_mark = "✓ " if f"{step_id}:{tid}" in st.session_state.result_cache else ""
        ttitle = t.get("title") if lang == "vi" else t.get("title_en")
        labels[tid] = f"{done_mark}{i+1}. {ttitle}"
    current = st.session_state.task_id
    if current not in task_options:
        current = STEP_OVERVIEW
        st.session_state.task_id = current

    picked = st.radio(
        _t("Công việc trong bước", "Tasks in this step", lang),
        options=task_options,
        format_func=lambda x: labels.get(x, x),
        horizontal=True,
        key=f"task_radio_{step_id}",
        index=task_options.index(current),
    )
    if picked != st.session_state.task_id:
        st.session_state.task_id = picked
        st.session_state.last_payload = st.session_state.result_cache.get(f"{step_id}:{picked}")
        st.rerun()

    task_id = st.session_state.task_id
    is_overview = task_id == STEP_OVERVIEW

    if tasks:
        done = sum(
            1 for t in tasks if f"{step_id}:{t['id']}" in st.session_state.result_cache
        )
        st.caption(
            _t(
                f"Tiến độ bước: {done}/{len(tasks)} công việc đã chạy",
                f"Step progress: {done}/{len(tasks)} tasks run",
                lang,
            )
        )
        if is_overview and st.button(
            _t("▶ Chạy tất cả task trong bước", "▶ Run all tasks in step", lang),
            use_container_width=True,
        ):
            params = {
                "query": SAMPLE_QUERIES[0],
                "top_k": DEFAULT_TOP_K,
                "enable_temporal": True,
                "enable_graph": True,
                "enable_trust_score": True,
            }
            prog = st.progress(0.0)
            for i, tsk in enumerate(tasks):
                tid = tsk["id"]
                ck = f"{step_id}:{tid}"
                try:
                    payload = core["pipeline"].run_task(step_id, tid, params)
                    st.session_state.result_cache[ck] = payload
                except Exception as e:  # noqa: BLE001
                    st.warning(f"{tid}: {e}")
                prog.progress((i + 1) / max(len(tasks), 1))
            st.success(_t("Đã chạy xong các task trong bước.", "Finished running step tasks.", lang))
            st.rerun()

    if is_overview:
        st.markdown(f"#### {_t('Các công việc con theo trình tự', 'Child tasks in order', lang)}")
        for i, t in enumerate(tasks, 1):
            ran = f"{step_id}:{t['id']}" in st.session_state.result_cache
            status = _t("đã chạy", "done", lang) if ran else _t("chưa chạy", "pending", lang)
            ttitle = t.get("title") if lang == "vi" else t.get("title_en")
            st.markdown(f"{i}. **{ttitle}** · `{status}` · `{t['id']}`")
        st.info(
            _t(
                "Chọn một công việc ở trên để xem khung học thuật và chạy thực nghiệm.",
                "Select a child task above to view the academic frame and run the experiment.",
                lang,
            )
        )
        try:
            pack = core["pipeline"].academic(step_id, None)
            _render_academic(pack if isinstance(pack, dict) else None, lang)
        except Exception as e:  # noqa: BLE001
            st.warning(str(e))
        return

    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        st.error("Unknown task")
        return

    ttitle = task.get("title") if lang == "vi" else task.get("title_en")
    st.markdown(
        f"**{_t(f'Công việc {task_options.index(task_id)}/{len(tasks)}', f'Task {task_options.index(task_id)}/{len(tasks)}', lang)}:** {ttitle}"
    )

    try:
        pack = core["pipeline"].academic(step_id, task_id)
        hide = f"{step_id}:{task_id}" in st.session_state.result_cache
        _render_academic(pack if isinstance(pack, dict) else None, lang, hide_assess=hide)
    except Exception as e:  # noqa: BLE001
        st.warning(str(e))

    cache_key = f"{step_id}:{task_id}"
    if (
        step_id == 1
        and task_id in {"catalog", "matrix"}
        and cache_key not in st.session_state.result_cache
    ):
        with st.spinner(_t("Đang tải catalog/matrix…", "Loading catalog/matrix…", lang)):
            try:
                payload = core["pipeline"].run_task(step_id, task_id, {})
                st.session_state.result_cache[cache_key] = payload
                st.session_state.last_payload = payload
            except Exception as e:  # noqa: BLE001
                st.error(str(e))

    with st.form(f"run_{step_id}_{task_id}"):
        st.markdown(f"#### {_t('Chạy thực nghiệm', 'Run experiment', lang)}")
        q_choice = st.selectbox(
            _t("Query mẫu", "Sample query", lang),
            SAMPLE_QUERIES,
            index=0,
        )
        custom = st.text_input(_t("Hoặc query tuỳ chỉnh", "Or custom query", lang), "")
        top_k = st.select_slider("top_k", options=TOP_K_CHOICES, value=DEFAULT_TOP_K)
        if step_id in ABLATION_STEPS:
            c1, c2, c3 = st.columns(3)
            enable_temporal = c1.checkbox("temporal", value=True)
            enable_graph = c2.checkbox("graph", value=True)
            enable_trust = c3.checkbox("trust_score", value=True)
        else:
            enable_temporal, enable_graph, enable_trust = True, True, True
            st.caption(
                _t(
                    "Ablation (temporal/graph/trust) chỉ hiện ở bước 4/6/8/9/11 — giống React.",
                    "Ablation toggles only on steps 4/6/8/9/11 — matching React.",
                    lang,
                )
            )
        submitted = st.form_submit_button(
            _t("Chạy task", "Run task", lang),
            type="primary",
            use_container_width=True,
        )

    if submitted:
        params = {
            "query": (custom or q_choice).strip(),
            "top_k": int(top_k),
            "enable_temporal": enable_temporal,
            "enable_graph": enable_graph,
            "enable_trust_score": enable_trust,
        }
        heavy = step_id in {9, 10, 11}
        spinner = (
            _t("Đang chạy (bước đánh giá có thể lâu)…", "Running (evaluation may take a while)…", lang)
            if heavy
            else _t("Đang chạy…", "Running…", lang)
        )
        try:
            with st.spinner(spinner):
                payload = core["pipeline"].run_task(step_id, task_id, params)
            st.session_state.result_cache[cache_key] = payload
            st.session_state.last_payload = payload
            st.success(
                _t(
                    f"Xong: bước {payload.get('step_id')} / {payload.get('task_id')} · {payload.get('elapsed_ms')} ms",
                    f"Done: step {payload.get('step_id')} / {payload.get('task_id')} · {payload.get('elapsed_ms')} ms",
                    lang,
                )
            )
        except Exception as e:  # noqa: BLE001
            st.error(str(e))
            st.exception(e)

    payload = st.session_state.last_payload or st.session_state.result_cache.get(cache_key)
    if not payload:
        return

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("elapsed_ms", payload.get("elapsed_ms"))
    m2.metric(
        _t("tính toán thật", "real computation", lang),
        "yes" if payload.get("real_computation") else "no",
    )
    m3.metric("kind", str(payload.get("computation_kind", "—")))
    m4.metric("action", str(payload.get("action", "—")))

    review = payload.get("result_review")
    if isinstance(review, dict):
        _render_result_review(review, lang)

    acad = payload.get("academic")
    if isinstance(acad, dict):
        st.markdown(f"#### {_t('Khung học thuật (sau chạy)', 'Academic (post-run)', lang)}")
        _render_academic(acad, lang, hide_assess=True)

    st.markdown(f"### {_t('Kết quả', 'Result', lang)}")
    parity.render_result_payload(
        payload.get("result", payload),
        lang,
        review if isinstance(review, dict) else None,
    )


def page_ids_cti(core: dict[str, Any], lang: str) -> None:
    _step_badge(16, _t("Ứng dụng IDS/CTI (live EDGR)", "Live IDS/CTI application", lang))
    status = core["app_status"]()
    st.caption(status.get("note_vi") if lang == "vi" else status.get("note_en"))
    _health_cards(core, lang)

    mode = st.radio(
        _t("Chế độ nhập", "Input mode", lang),
        options=["alert", "query"],
        format_func=lambda m: _t("Alert realtime (Suricata)", "Realtime alert (Suricata)", lang)
        if m == "alert"
        else _t("Truy vấn CTI", "CTI query", lang),
        horizontal=True,
        key="ids_mode_radio",
        index=0 if st.session_state.ids_mode == "alert" else 1,
    )
    st.session_state.ids_mode = mode

    top_k = st.select_slider(
        "top_k",
        options=TOP_K_CHOICES,
        value=DEFAULT_TOP_K,
        key="ids_topk",
    )

    if mode == "query":
        if "ids_query_area" not in st.session_state:
            st.session_state.ids_query_area = SAMPLE_QUERIES[0]
        qc = st.columns(len(QUICK_QUERIES))
        for col, item in zip(qc, QUICK_QUERIES):
            with col:
                if st.button(
                    item["label_vi"] if lang == "vi" else item["label_en"],
                    key=f"qq_{item['id']}",
                    use_container_width=True,
                ):
                    st.session_state.ids_query_area = item["q"]
                    st.rerun()

        with st.form("analyze_form"):
            query = st.text_area(
                _t("Query", "Query", lang),
                height=90,
                key="ids_query_area",
            )
            c1, c2, c3, c4 = st.columns(4)
            enable_temporal = c1.checkbox("temporal", value=True, key="a_t")
            enable_graph = c2.checkbox("graph", value=True, key="a_g")
            enable_trust = c3.checkbox("trust_score", value=True, key="a_s")
            live_enrich = c4.checkbox("NVD live enrich", value=True, key="a_n")
            submitted = st.form_submit_button(
                _t("Phân tích (live EDGR)", "Analyze (live EDGR)", lang),
                type="primary",
                use_container_width=True,
            )
        if submitted:
            try:
                with st.spinner(_t("Đang chạy EDGR…", "Running EDGR…", lang)):
                    out = core["analyze"](
                        query.strip(),
                        top_k=int(top_k),
                        enable_temporal=enable_temporal,
                        enable_graph=enable_graph,
                        enable_trust_score=enable_trust,
                        live_enrich=live_enrich,
                    )
                st.session_state.ids_result = out
            except Exception as e:  # noqa: BLE001
                st.error(str(e))
                st.exception(e)
    else:
        ai = core["alert_ingest"]
        sample = ai.sample_alert_payload()
        default_json = json.dumps(sample.get("alert") or {}, ensure_ascii=False, indent=2)
        alert_json = st.text_area(
            _t("JSON alert (Suricata eve-style)", "Alert JSON (Suricata eve-style)", lang),
            value=st.session_state.get("alert_json_text", default_json),
            height=220,
            key="alert_json_area",
        )
        b1, b2, b3 = st.columns(3)
        if b1.button(_t("Nạp mẫu", "Load sample", lang), use_container_width=True):
            st.session_state.alert_json_text = default_json
            st.rerun()
        ingest_only = b2.button(_t("Ingest", "Ingest", lang), use_container_width=True)
        ingest_run = b3.button(
            _t("Ingest + Analyze", "Ingest + Analyze", lang),
            type="primary",
            use_container_width=True,
        )

        if ingest_only or ingest_run:
            try:
                payload = json.loads(alert_json)
                ing = ai.ingest_alerts(payload)
                st.success(
                    _t(
                        f"Đã nạp · queue={ing.get('queue_size')}",
                        f"Ingested · queue={ing.get('queue_size')}",
                        lang,
                    )
                )
                alerts = (ing.get("alerts") or [])
                if alerts:
                    st.session_state.selected_alert_id = alerts[0].get("id")
                if ingest_run and st.session_state.selected_alert_id:
                    with st.spinner(_t("Đang analyze alert…", "Analyzing alert…", lang)):
                        st.session_state.ids_result = core["analyze_alert"](
                            st.session_state.selected_alert_id,
                            top_k=int(top_k),
                            live_enrich=True,
                        )
            except Exception as e:  # noqa: BLE001
                st.error(str(e))

        listed = ai.list_alerts(limit=40)
        alerts = listed.get("alerts") or []
        st.caption(
            _t(
                f"Hàng đợi alert: {listed.get('queue_size', 0)}",
                f"Alert queue: {listed.get('queue_size', 0)}",
                lang,
            )
        )
        if alerts:
            labels = {
                a["id"]: f"{a.get('id','')[:8]}… · {str(a.get('query') or a.get('signature') or '')[:60]}"
                for a in alerts
                if a.get("id")
            }
            ids = list(labels.keys())
            sel = st.selectbox(
                _t("Chọn alert", "Select alert", lang),
                options=ids,
                format_func=lambda i: labels.get(i, i),
                index=ids.index(st.session_state.selected_alert_id)
                if st.session_state.selected_alert_id in ids
                else 0,
            )
            st.session_state.selected_alert_id = sel
            if st.button(_t("Analyze alert đã chọn", "Analyze selected alert", lang), type="primary"):
                try:
                    with st.spinner(_t("Đang analyze alert…", "Analyzing alert…", lang)):
                        st.session_state.ids_result = core["analyze_alert"](
                            sel, top_k=int(top_k), live_enrich=True
                        )
                except Exception as e:  # noqa: BLE001
                    st.error(str(e))

    out = st.session_state.ids_result
    if not out:
        return

    is_live = out.get("simulated") is False or out.get("mode") == "live_edgr"
    if is_live:
        st.success(_t("Live EDGR · không phải đáp án giả lập", "Live EDGR · not a scripted answer", lang))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("confidence", _cell(out.get("confidence"), "confidence") or "—")
    m2.metric("faithfulness", _cell(out.get("faithfulness"), "faithfulness") or "—")
    m3.metric("hallucination", _cell(out.get("hallucination_rate"), "hallucination_rate") or "—")
    m4.metric("latency_ms", out.get("latency_ms"))

    if out.get("abstained"):
        st.warning(_pick(out, "abstain_reason_vi", "abstain_reason_en", lang))
        if out.get("apply") == 0 or out.get("trusted") is False:
            st.info(
                _t(
                    "Apply = 0 · cổng tin cậy từ chối Trusted Answer (giống React).",
                    "Apply = 0 · trust gate refused Trusted Answer (matches React).",
                    lang,
                )
            )

    stages = out.get("stage_summary") or out.get("stages")
    if isinstance(stages, list) and stages:
        pills = []
        for i, s in enumerate(stages, 1):
            if isinstance(s, dict):
                name = s.get("name_vi" if lang == "vi" else "name") or s.get("name") or s.get("stage") or i
                dur = s.get("duration_ms")
                extra = f" · {dur}ms" if dur is not None else ""
                pills.append(f'<span class="stage-pill">{i}. {name}{extra}</span>')
            else:
                pills.append(f'<span class="stage-pill">{i}. {s}</span>')
        st.markdown(
            f"**{_t('Giai đoạn EDGR', 'EDGR stages', lang)}**"
            f'<div class="stage-row">{"".join(pills)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(f"**{_t('Câu trả lời', 'Answer', lang)}**")
    st.write(out.get("answer") or "—")

    ents = out.get("entities") or []
    if ents:
        st.caption("Entities: " + ", ".join(map(str, ents[:16])))

    evid = out.get("evidence") or []
    if evid:
        st.markdown(f"**{_t('Bằng chứng', 'Evidence', lang)}** ({len(evid)})")
        for i, e in enumerate(evid[: top_k + 3], 1):
            if isinstance(e, dict):
                st.markdown(
                    f"{i}. score=`{_cell(e.get('score', e.get('trust_score')), 'score')}` — "
                    f"{e.get('text') or e.get('content') or e.get('id') or e}"
                )
            else:
                st.markdown(f"{i}. {e}")

    for viz in _gather_viz(out):
        _render_viz_block(viz, lang)

    enrich = out.get("live_enrichment")
    if isinstance(enrich, dict) and enrich.get("attempted"):
        with st.expander("NVD live enrichment"):
            st.json(enrich)

    with st.expander(_t("Payload đầy đủ", "Full payload", lang)):
        st.code(json.dumps(out, ensure_ascii=False, indent=2, default=str)[:120_000])


def main() -> None:
    _init_state()
    on_cloud = _is_streamlit_cloud()

    lang = st.sidebar.radio(
        _t("Ngôn ngữ", "Language", st.session_state.lang),
        options=["vi", "en"],
        format_func=lambda x: "Tiếng Việt" if x == "vi" else "English",
        horizontal=True,
        index=0 if st.session_state.lang == "vi" else 1,
        key="lang_radio",
    )
    st.session_state.lang = lang

    if on_cloud:
        mode = "native"
        st.session_state.ui_mode = "native"
        st.sidebar.caption(
            _t(
                "Streamlit Cloud: dùng UI native (React iframe cần FastAPI localhost — không public được).",
                "Streamlit Cloud: native UI only (React iframe needs local FastAPI — not publicly reachable).",
                lang,
            )
        )
    else:
        mode = st.sidebar.radio(
            _t("Chế độ UI", "UI mode", lang),
            options=["react", "native"],
            format_func=lambda m: _t(
                "React gốc (y hệt SPA)",
                "Real React (pixel-perfect SPA)",
                lang,
            )
            if m == "react"
            else _t("Streamlit native (gần đúng)", "Streamlit native (approximate)", lang),
            index=0 if st.session_state.ui_mode == "react" else 1,
            key="ui_mode_radio",
        )
        st.session_state.ui_mode = mode
        st.sidebar.caption(
            _t(
                "Mặc định nhúng React qua iframe FastAPI `/ui/` — layout/CSS/chức năng như bản cũ.",
                "Default embeds React via FastAPI `/ui/` iframe — same layout/CSS/behavior as the SPA.",
                lang,
            )
        )

    if mode == "react":
        page_react_embed(lang)
        return

    # ── Native Streamlit path (approximate) ───────────────────────────
    _inject_css()

    try:
        core = _load_core()
    except Exception as e:  # noqa: BLE001
        st.error(_t("Không tải được core EDGR", "Failed to load EDGR core", lang))
        st.exception(e)
        return

    definition = core["pipeline"].definition()
    steps = definition.get("steps") or []
    stats = core["kg"].stats()
    health_line = _t(
        f"{len(steps)} bước · {stats.nodes} nút · {len(core['vector_store'].chunks)} bằng chứng",
        f"{len(steps)} steps · {stats.nodes} nodes · {len(core['vector_store'].chunks)} evidence",
        lang,
    )
    # Count unique step completions (any task cached for that step)
    completed_steps = set()
    for key in st.session_state.result_cache:
        try:
            completed_steps.add(int(str(key).split(":", 1)[0]))
        except ValueError:
            pass
    _hero(lang, health_line, done=len(completed_steps), total=len(steps))

    # Top step rail (closer to React StepRail) + sidebar
    st.markdown('<div class="step-rail-top">', unsafe_allow_html=True)
    rail_cols = st.columns(min(9, len(steps) + 1))
    # Overview button
    with rail_cols[0]:
        if st.button("0", key="rail_0", help=_t("Tổng quan", "Overview", lang), use_container_width=True):
            st.session_state.step_id = 0
            st.session_state.task_id = STEP_OVERVIEW
            st.session_state.last_payload = None
            st.rerun()
    for i, s in enumerate(steps[:8]):
        sid = int(s["id"])
        with rail_cols[(i + 1) % len(rail_cols)]:
            mark = "✓" if sid in completed_steps else str(sid)
            if st.button(
                mark,
                key=f"rail_{sid}",
                help=(s.get("title") if lang == "vi" else s.get("title_en")),
                use_container_width=True,
                type="primary" if st.session_state.step_id == sid else "secondary",
            ):
                st.session_state.step_id = sid
                st.session_state.task_id = STEP_OVERVIEW
                st.session_state.last_payload = None
                st.rerun()
    if len(steps) > 8:
        rail2 = st.columns(min(8, len(steps) - 8))
        for i, s in enumerate(steps[8:]):
            sid = int(s["id"])
            with rail2[i % len(rail2)]:
                mark = "✓" if sid in completed_steps else str(sid)
                if st.button(
                    mark,
                    key=f"rail2_{sid}",
                    help=(s.get("title") if lang == "vi" else s.get("title_en")),
                    use_container_width=True,
                    type="primary" if st.session_state.step_id == sid else "secondary",
                ):
                    st.session_state.step_id = sid
                    st.session_state.task_id = STEP_OVERVIEW
                    st.session_state.last_payload = None
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar step rail
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"**{_t('Quy trình nghiên cứu', 'Research pipeline', lang)}**"
    )
    nav_labels = [_t("0 · Tổng quan", "0 · Overview", lang)]
    nav_ids = [0]
    for s in steps:
        sid = int(s["id"])
        ttitle = s.get("title") if lang == "vi" else s.get("title_en")
        short = (ttitle or "")[:28]
        done = "✓ " if sid in completed_steps else ""
        nav_labels.append(f"{done}{sid} · {short}")
        nav_ids.append(sid)

    try:
        idx = nav_ids.index(st.session_state.step_id)
    except ValueError:
        idx = 0

    choice = st.sidebar.radio(
        _t("Chọn bước", "Select step", lang),
        options=nav_ids,
        format_func=lambda i: nav_labels[nav_ids.index(i)],
        index=idx,
        key="step_rail",
    )
    if choice != st.session_state.step_id:
        st.session_state.step_id = choice
        st.session_state.task_id = STEP_OVERVIEW
        st.session_state.last_payload = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown(_t("**Trạng thái store**", "**Store status**", lang))
    st.sidebar.write(
        {
            "kg_nodes": stats.nodes,
            "kg_edges": stats.edges,
            "evidence": len(core["vector_store"].chunks),
            "qa_pairs": core["qa_n"],
            "cached_tasks": len(st.session_state.result_cache),
        }
    )
    st.sidebar.caption(
        _t(
            "Cùng core Python với React/FastAPI — không mock. "
            "UI Streamlit bám React tối đa trong giới hạn widget (không pixel-perfect SPA).",
            "Same Python core as React/FastAPI — no mocks. "
            "Streamlit UI mirrors React as far as widgets allow (not pixel-perfect SPA).",
            lang,
        )
    )

    step_id = st.session_state.step_id
    if step_id == 0:
        page_overview(core, lang)
    elif step_id == 16:
        page_ids_cti(core, lang)
    else:
        page_step(core, lang, step_id)


main()
