"""Chart visualization payloads for analysis tabs (time, convergence, scalability)."""

from __future__ import annotations

from typing import Any


def bar_chart_viz(
    *,
    title_vi: str,
    title_en: str,
    caption_vi: str = "",
    caption_en: str = "",
    y_label_vi: str,
    y_label_en: str,
    bars: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    bars: [{label_vi, label_en, value}, ...]
    """
    return {
        "kind": "bar_chart",
        "title_vi": title_vi,
        "title_en": title_en,
        "caption_vi": caption_vi,
        "caption_en": caption_en,
        "y_label_vi": y_label_vi,
        "y_label_en": y_label_en,
        "bars": bars,
    }


def line_chart_viz(
    *,
    title_vi: str,
    title_en: str,
    caption_vi: str = "",
    caption_en: str = "",
    x_label_vi: str,
    x_label_en: str,
    points: list[dict[str, Any]],
    series: list[dict[str, str]],
) -> dict[str, Any]:
    """
    points: [{x: number, <y_key>: number, ...}, ...]
    series: [{key, label_vi, label_en}, ...]
    """
    return {
        "kind": "line_chart",
        "title_vi": title_vi,
        "title_en": title_en,
        "caption_vi": caption_vi,
        "caption_en": caption_en,
        "x_label_vi": x_label_vi,
        "x_label_en": x_label_en,
        "points": points,
        "series": series,
    }


def convergence_chart(series_rows: list[dict[str, Any]]) -> dict[str, Any]:
    points = [
        {
            "x": int(r.get("top_k", i + 1)),
            "prefix_stability": float(r.get("prefix_stability", 0) or 0),
            "faithfulness": float(r.get("faithfulness", 0) or 0),
        }
        for i, r in enumerate(series_rows)
    ]
    return line_chart_viz(
        title_vi="Biểu đồ hội tụ thực nghiệm (theo top-k)",
        title_en="Empirical convergence chart (vs top-k)",
        caption_vi=(
            "prefix_stability: độ chồng lắp tập evidence khi tăng k; "
            "faithfulness: điểm neo bằng chứng. Hội tụ khi đường ổn định ở các mốc k lớn."
        ),
        caption_en=(
            "prefix_stability: evidence-set overlap as k grows; "
            "faithfulness: grounding score. Convergence when curves stabilize at larger k."
        ),
        x_label_vi="top_k",
        x_label_en="top_k",
        points=points,
        series=[
            {
                "key": "prefix_stability",
                "label_vi": "Prefix stability",
                "label_en": "Prefix stability",
            },
            {
                "key": "faithfulness",
                "label_vi": "Faithfulness",
                "label_en": "Faithfulness",
            },
        ],
    )


def time_complexity_charts(
    stages: list[dict[str, Any]],
    latency_by_k: list[dict[str, Any]],
    *,
    V: int,
    E: int,
) -> dict[str, Any]:
    """
    Analyze(time) visuals:
    1) Stage wall-clock bars — empirical T breakdown of one EDGR run
    2) Latency vs top_k — how ranking/selection time grows with k
    """
    import math

    bars = []
    for s in stages:
        stage_no = s.get("stage", "")
        name = str(s.get("name") or f"φ{stage_no}")
        bars.append(
            {
                "label_vi": f"φ{stage_no} {name}",
                "label_en": f"φ{stage_no} {name}",
                "value": float(s.get("duration_ms", 0) or 0),
            }
        )

    stage_bar = bar_chart_viz(
        title_vi="Phân bổ thời gian theo giai đoạn EDGR",
        title_en="EDGR stage time breakdown",
        caption_vi=(
            f"Thời gian wall-clock (ms) từng giai đoạn trên KG live (V={V}, E={E}). "
            f"Đối chiếu biên tiệm cận T(n)=O(E log V) ≈ {E}·log₂({max(V, 1)}) "
            f"≈ {round(E * math.log(max(V, 1), 2), 1)}."
        ),
        caption_en=(
            f"Wall-clock ms per stage on the live KG (V={V}, E={E}). "
            f"Asymptotic reference T(n)=O(E log V) ≈ {E}·log₂({max(V, 1)}) "
            f"≈ {round(E * math.log(max(V, 1), 2), 1)}."
        ),
        y_label_vi="Thời gian (ms)",
        y_label_en="Time (ms)",
        bars=bars,
    )

    points = [
        {
            "x": int(r.get("top_k", i + 1)),
            "latency_ms": float(r.get("latency_ms", 0) or 0),
        }
        for i, r in enumerate(latency_by_k)
    ]
    growth = line_chart_viz(
        title_vi="Độ phức tạp thời gian thực nghiệm (latency theo top_k)",
        title_en="Empirical time complexity (latency vs top_k)",
        caption_vi=(
            "Tổng latency EDGR khi tăng ngân sách evidence k. "
            "Phản ánh chi phí xếp hạng/chọn lọc (thành phần gần O(k log k) + fuse đồ thị); "
            "không nhầm với biểu đồ hội tụ (prefix stability)."
        ),
        caption_en=(
            "Total EDGR latency as evidence budget k grows. "
            "Reflects ranking/selection cost (near O(k log k) + graph fuse); "
            "not the convergence chart (prefix stability)."
        ),
        x_label_vi="top_k",
        x_label_en="top_k",
        points=points,
        series=[
            {
                "key": "latency_ms",
                "label_vi": "Latency (ms)",
                "label_en": "Latency (ms)",
            },
        ],
    )

    charts = [stage_bar, growth]
    return {
        "kind": "multi_chart",
        "title_vi": "Biểu đồ phân tích thời gian Analyze(time)",
        "title_en": "Analyze(time) charts",
        "charts": charts,
    }


def scalability_chart(scale_rows: list[dict[str, Any]]) -> dict[str, Any]:
    # Latency only on the Y-axis (ms); faithfulness stays in the table (different scale).
    points = [
        {
            "x": int(r.get("evidence_corpus_size", 0) or 0),
            "latency_ms": float(r.get("latency_ms", 0) or 0),
        }
        for r in scale_rows
    ]
    return line_chart_viz(
        title_vi="Biểu đồ khả năng mở rộng (latency theo |D|)",
        title_en="Scalability chart (latency vs |D|)",
        caption_vi="Latency (ms) khi tăng kích thước corpus evidence |D|. Faithfulness xem bảng số liệu.",
        caption_en="Latency (ms) as evidence corpus size |D| grows. See the table for faithfulness.",
        x_label_vi="|D| (evidence chunks)",
        x_label_en="|D| (evidence chunks)",
        points=points,
        series=[
            {
                "key": "latency_ms",
                "label_vi": "Latency (ms)",
                "label_en": "Latency (ms)",
            },
        ],
    )
