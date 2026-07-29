import { useMemo } from "react";
import { csvFilename, downloadCsv } from "./downloadCsv";
import { useLocale } from "./i18n/LocaleContext";

type MatrixBlock = {
  title: string;
  rowLabels: string[];
  colLabels: string[];
  values: number[][];
  binary?: boolean;
};

type GraphNode = {
  id: string;
  label?: string;
  type?: string;
  seed?: boolean;
};

type GraphEdge = {
  source: string;
  target: string;
  relation?: string;
  weight?: number;
};

type PickFn = (vi: string, en: string) => string;

function asRecord(v: unknown): Record<string, unknown> | null {
  return v && typeof v === "object" && !Array.isArray(v)
    ? (v as Record<string, unknown>)
    : null;
}

function cellColor(v: number, max: number, binary?: boolean): string {
  if (binary) {
    return v > 0 ? "rgba(14, 116, 144, 0.85)" : "rgba(148, 163, 184, 0.18)";
  }
  if (max <= 0 || v <= 0) return "rgba(148, 163, 184, 0.14)";
  const t = Math.min(1, v / max);
  const r = Math.round(14 + t * 200);
  const g = Math.round(116 - t * 40);
  const b = Math.round(144 - t * 100);
  const a = 0.25 + t * 0.7;
  return `rgba(${r},${g},${b},${a})`;
}

export function MatrixHeatmap({ block }: { block: MatrixBlock }) {
  const { t } = useLocale();
  const max = useMemo(() => {
    let m = 0;
    for (const row of block.values) {
      for (const v of row) m = Math.max(m, Number(v) || 0);
    }
    return m;
  }, [block.values]);

  const nR = block.rowLabels.length;
  const nC = block.colLabels.length;
  if (!nR || !nC) return null;

  const onDownload = () => {
    downloadCsv(
      csvFilename(block.title, "matrix"),
      ["row", ...block.colLabels],
      block.rowLabels.map((r, i) => [
        r,
        ...block.colLabels.map((_, j) => Number(block.values[i]?.[j] ?? 0) || 0),
      ]),
    );
  };

  return (
    <figure className="viz-matrix">
      <div className="viz-matrix-head">
        <figcaption>{block.title}</figcaption>
        <button
          type="button"
          className="table-dl-btn"
          onClick={onDownload}
          title={t("table_download")}
        >
          {t("table_download")}
        </button>
      </div>
      <div className="viz-matrix-scroll">
        <table className="heatmap-table">
          <thead>
            <tr>
              <th className="corner" />
              {block.colLabels.map((c) => (
                <th key={c} title={c}>
                  <span>{c}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {block.rowLabels.map((r, i) => (
              <tr key={r}>
                <th title={r}>
                  <span>{r}</span>
                </th>
                {block.colLabels.map((c, j) => {
                  const v = Number(block.values[i]?.[j] ?? 0) || 0;
                  return (
                    <td
                      key={`${r}-${c}`}
                      style={{ background: cellColor(v, max, block.binary) }}
                      title={`${r} × ${c} = ${v}`}
                    >
                      <span className={v === 0 ? "zero" : ""}>{v}</span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="viz-legend">
        {block.binary ? (
          <>
            <span className="swatch off" /> 0
            <span className="swatch on" /> 1
          </>
        ) : (
          <>
            <span className="swatch low" /> 0
            <span className="swatch mid" /> …
            <span className="swatch high" /> {max}
          </>
        )}
      </div>
    </figure>
  );
}

function shortLabel(raw: string, max = 16): string {
  const s = raw.trim();
  if (s.length <= max) return s;
  return `${s.slice(0, Math.max(4, max - 1))}…`;
}

/** Place text outward from graph center to reduce label pile-ups. */
function outwardLabelPos(
  x: number,
  y: number,
  cx: number,
  cy: number,
  dist: number,
): { x: number; y: number; anchor: "start" | "middle" | "end" } {
  const dx = x - cx;
  const dy = y - cy;
  const len = Math.hypot(dx, dy) || 1;
  const ux = dx / len;
  const uy = dy / len;
  const lx = x + ux * dist;
  const ly = y + uy * dist;
  let anchor: "start" | "middle" | "end" = "middle";
  if (ux > 0.35) anchor = "start";
  else if (ux < -0.35) anchor = "end";
  return { x: lx, y: ly, anchor };
}

function layoutGraph(nodes: GraphNode[], width: number, height: number) {
  const n = nodes.length;
  if (n === 0) return new Map<string, { x: number; y: number }>();
  const cx = width / 2;
  const cy = height / 2;
  const pad = 56;
  const rMax = Math.min(width, height) / 2 - pad;
  const pos = new Map<string, { x: number; y: number }>();

  const seeds = nodes.filter((x) => x.seed);
  const others = nodes.filter((x) => !x.seed);
  const seedR = seeds.length <= 1 ? 0 : Math.min(52, rMax * 0.28);
  seeds.forEach((s, i) => {
    const a =
      (2 * Math.PI * i) / Math.max(seeds.length, 1) - Math.PI / 2;
    pos.set(s.id, {
      x: cx + seedR * Math.cos(a),
      y: cy + seedR * Math.sin(a),
    });
  });

  // Spread non-seeds on 1–2 outer rings by index (larger gap than before).
  const ringCount = others.length > 14 ? 2 : 1;
  others.forEach((node, i) => {
    const ringIdx = ringCount === 1 ? 0 : i % ringCount;
    const onRing = others.filter((_, j) =>
      ringCount === 1 ? true : j % ringCount === ringIdx,
    );
    const k = onRing.findIndex((x) => x.id === node.id);
    const a =
      (2 * Math.PI * k) / Math.max(onRing.length, 1) -
      Math.PI / 2 +
      (ringIdx === 1 ? Math.PI / onRing.length : 0);
    const ring = rMax * (ringCount === 1 ? 0.88 : 0.62 + ringIdx * 0.3);
    pos.set(node.id, {
      x: cx + ring * Math.cos(a),
      y: cy + ring * Math.sin(a),
    });
  });

  // Simple repulsion pass to separate near-duplicates.
  const ids = nodes.map((n) => n.id);
  for (let iter = 0; iter < 40; iter++) {
    for (let i = 0; i < ids.length; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        const a = pos.get(ids[i])!;
        const b = pos.get(ids[j])!;
        let dx = a.x - b.x;
        let dy = a.y - b.y;
        let d = Math.hypot(dx, dy);
        const minD = 54;
        if (d < 1e-3) {
          dx = Math.cos(i + j) * 2;
          dy = Math.sin(i + j) * 2;
          d = Math.hypot(dx, dy);
        }
        if (d < minD) {
          const push = ((minD - d) / d) * 0.5;
          a.x += dx * push;
          a.y += dy * push;
          b.x -= dx * push;
          b.y -= dy * push;
        }
      }
    }
    // Keep inside frame.
    for (const id of ids) {
      const p = pos.get(id)!;
      p.x = Math.min(width - 36, Math.max(36, p.x));
      p.y = Math.min(height - 28, Math.max(28, p.y));
    }
  }
  return pos;
}

const TYPE_COLOR: Record<string, string> = {
  cve: "#b45309",
  technique: "#0e7490",
  tactic: "#0369a1",
  malware: "#be123c",
  actor: "#7c3aed",
  entity: "#334155",
  unknown: "#64748b",
};

export function GraphNetwork({
  title,
  nodes,
  edges,
}: {
  title: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
}) {
  const { t } = useLocale();
  const W = 780;
  const H = 480;
  const cx = W / 2;
  const cy = H / 2;
  const pos = useMemo(() => layoutGraph(nodes, W, H), [nodes]);
  const idSet = useMemo(() => new Set(nodes.map((n) => n.id)), [nodes]);
  const drawnEdges = edges.filter(
    (e) => idSet.has(e.source) && idSet.has(e.target),
  );

  // Hide edge labels when dense; keep unique mid-edge labels with perpendicular offset.
  const showEdgeLabels = drawnEdges.length <= 18 && nodes.length <= 22;
  const edgeLabelSlots = useMemo(() => {
    if (!showEdgeLabels) return [] as Array<{
      key: string;
      x: number;
      y: number;
      text: string;
      full: string;
    }>;
    const used = new Map<string, number>();
    const out: Array<{
      key: string;
      x: number;
      y: number;
      text: string;
      full: string;
    }> = [];
    drawnEdges.forEach((e, i) => {
      if (!e.relation) return;
      const a = pos.get(e.source);
      const b = pos.get(e.target);
      if (!a || !b) return;
      const mx = (a.x + b.x) / 2;
      const my = (a.y + b.y) / 2;
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const len = Math.hypot(dx, dy) || 1;
      const px = -dy / len;
      const py = dx / len;
      const pairKey = [e.source, e.target].sort().join("|");
      const slot = used.get(pairKey) ?? 0;
      used.set(pairKey, slot + 1);
      const bump = 10 + slot * 11;
      out.push({
        key: `el-${i}`,
        x: mx + px * bump,
        y: my + py * bump,
        text: shortLabel(e.relation, 14),
        full: e.relation,
      });
    });
    return out;
  }, [drawnEdges, pos, showEdgeLabels]);

  if (nodes.length === 0) {
    return <p className="muted">{t("viz_graph_empty")}</p>;
  }

  return (
    <figure className="viz-graph">
      <figcaption>
        {title}
        <span className="viz-meta">
          {nodes.length} {t("viz_nodes")} · {drawnEdges.length} {t("viz_edges")}
          {!showEdgeLabels ? ` · ${t("viz_labels_compact")}` : ""}
        </span>
      </figcaption>
      <svg viewBox={`0 0 ${W} ${H}`} className="graph-svg" role="img">
        <defs>
          <marker
            id="arrow"
            viewBox="0 0 10 10"
            refX="22"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(71,85,105,0.7)" />
          </marker>
        </defs>
        {drawnEdges.map((e, i) => {
          const a = pos.get(e.source);
          const b = pos.get(e.target);
          if (!a || !b) return null;
          return (
            <g key={`e-${i}`}>
              <title>{e.relation ? `${e.source} —${e.relation}→ ${e.target}` : `${e.source} → ${e.target}`}</title>
              <line
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                className="graph-edge"
                markerEnd="url(#arrow)"
              />
            </g>
          );
        })}
        {edgeLabelSlots.map((el) => (
          <text
            key={el.key}
            x={el.x}
            y={el.y}
            className="graph-edge-label"
          >
            <title>{el.full}</title>
            {el.text}
          </text>
        ))}
        {nodes.map((n) => {
          const p = pos.get(n.id);
          if (!p) return null;
          const fill = TYPE_COLOR[n.type || "entity"] || TYPE_COLOR.entity;
          const full = n.label || n.id;
          const lp = outwardLabelPos(p.x, p.y, cx, cy, n.seed ? 26 : 22);
          return (
            <g key={n.id} className={n.seed ? "graph-node seed" : "graph-node"}>
              <title>{`${full}${n.type ? ` (${n.type})` : ""}`}</title>
              <circle
                cx={p.x}
                cy={p.y}
                r={n.seed ? 15 : 11}
                fill={fill}
                stroke={n.seed ? "#0f172a" : "rgba(15,23,42,0.35)"}
                strokeWidth={n.seed ? 2.5 : 1}
              />
              <text
                x={lp.x}
                y={lp.y}
                className="graph-node-label"
                textAnchor={lp.anchor}
                dominantBaseline="middle"
              >
                {shortLabel(full, nodes.length > 18 ? 12 : 16)}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="viz-legend types">
        {Object.entries(TYPE_COLOR)
          .filter(([k]) => nodes.some((n) => (n.type || "entity") === k))
          .map(([k, c]) => (
            <span key={k}>
              <i style={{ background: c }} />
              {k}
            </span>
          ))}
      </div>
      {nodes.length > 12 ? (
        <ul className="graph-label-index">
          {nodes.map((n) => (
            <li key={n.id} title={n.label || n.id}>
              <i
                style={{
                  background:
                    TYPE_COLOR[n.type || "entity"] || TYPE_COLOR.entity,
                }}
              />
              <code>{shortLabel(n.id, 18)}</code>
              <span>{shortLabel(n.label || n.id, 28)}</span>
            </li>
          ))}
        </ul>
      ) : null}
    </figure>
  );
}

/** Keys already drawn as figures — omit from nested table dumps. */
export const VIZ_CONSUMED_KEYS = new Set([
  "viz",
  "pair_matrix",
  "incidence_matrix",
  "incidence_rows",
  "incidence_col_labels",
  "matrix",
  "extracted_nodes", // drawn as network when viz/fallback graph is present
  "architecture", // drawn when kind=architecture (also embedded in operating model)
  "charts", // multi_chart companion list
]);

const CHART_COLORS = ["#0f766e", "#b45309", "#0369a1", "#7c3aed", "#be123c"];

type LineSeriesDef = { key: string; label: string; color: string };

export type LineChartBlock = {
  title: string;
  caption: string;
  xLabel: string;
  points: Array<Record<string, number>>;
  series: LineSeriesDef[];
};

export type BarChartBlock = {
  title: string;
  caption: string;
  yLabel: string;
  bars: Array<{ label: string; value: number; color: string }>;
};

function parseLineChart(
  viz: Record<string, unknown>,
  pick: PickFn,
): LineChartBlock | null {
  if (viz.kind !== "line_chart") return null;
  const rawPoints = Array.isArray(viz.points) ? viz.points : [];
  const points = rawPoints.map((p) => {
    const r = asRecord(p) || {};
    const out: Record<string, number> = { x: Number(r.x) || 0 };
    for (const [k, v] of Object.entries(r)) {
      if (k === "x") continue;
      const n = Number(v);
      if (!Number.isNaN(n)) out[k] = n;
    }
    return out;
  });
  if (!points.length) return null;
  const rawSeries = Array.isArray(viz.series) ? viz.series : [];
  const series: LineSeriesDef[] = rawSeries.map((s, i) => {
    const r = asRecord(s) || {};
    return {
      key: String(r.key || ""),
      label: pick(String(r.label_vi || ""), String(r.label_en || r.label_vi || "")),
      color: CHART_COLORS[i % CHART_COLORS.length],
    };
  }).filter((s) => s.key);
  if (!series.length) return null;
  return {
    title: pick(
      String(viz.title_vi || "Biểu đồ"),
      String(viz.title_en || viz.title_vi || "Chart"),
    ),
    caption: pick(
      String(viz.caption_vi || ""),
      String(viz.caption_en || viz.caption_vi || ""),
    ),
    xLabel: pick(
      String(viz.x_label_vi || "x"),
      String(viz.x_label_en || viz.x_label_vi || "x"),
    ),
    points,
    series,
  };
}

export function LineChart({ block }: { block: LineChartBlock }) {
  const W = 520;
  const H = 260;
  const pad = { t: 20, r: 16, b: 36, l: 44 };
  const innerW = W - pad.l - pad.r;
  const innerH = H - pad.t - pad.b;

  const xs = block.points.map((p) => p.x);
  const xMin = Math.min(...xs);
  const xMax = Math.max(...xs);
  let yMin = Infinity;
  let yMax = -Infinity;
  for (const p of block.points) {
    for (const s of block.series) {
      const v = p[s.key];
      if (typeof v === "number" && !Number.isNaN(v)) {
        yMin = Math.min(yMin, v);
        yMax = Math.max(yMax, v);
      }
    }
  }
  if (!Number.isFinite(yMin) || !Number.isFinite(yMax)) {
    yMin = 0;
    yMax = 1;
  }
  if (yMin === yMax) {
    yMin = Math.max(0, yMin - 0.1);
    yMax = yMax + 0.1;
  }
  // Nice pad on y
  const yPad = (yMax - yMin) * 0.08;
  yMin = Math.max(0, yMin - yPad);
  yMax = yMax + yPad;

  const xScale = (x: number) =>
    pad.l + ((x - xMin) / (xMax - xMin || 1)) * innerW;
  const yScale = (y: number) =>
    pad.t + innerH - ((y - yMin) / (yMax - yMin || 1)) * innerH;

  const yTicks = 4;
  const tickVals = Array.from({ length: yTicks + 1 }, (_, i) =>
    yMin + ((yMax - yMin) * i) / yTicks,
  );

  return (
    <figure className="viz-line-chart">
      <figcaption>{block.title}</figcaption>
      {block.caption ? (
        <p className="chart-caption muted">{block.caption}</p>
      ) : null}
      <svg
        className="line-chart-svg"
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label={block.title}
      >
        {/* grid */}
        {tickVals.map((yv, i) => (
          <g key={i}>
            <line
              className="chart-grid"
              x1={pad.l}
              x2={pad.l + innerW}
              y1={yScale(yv)}
              y2={yScale(yv)}
            />
            <text
              className="chart-tick"
              x={pad.l - 6}
              y={yScale(yv) + 3}
              textAnchor="end"
            >
              {yv >= 10 ? yv.toFixed(0) : yv.toFixed(2)}
            </text>
          </g>
        ))}
        <line
          className="chart-axis"
          x1={pad.l}
          y1={pad.t}
          x2={pad.l}
          y2={pad.t + innerH}
        />
        <line
          className="chart-axis"
          x1={pad.l}
          y1={pad.t + innerH}
          x2={pad.l + innerW}
          y2={pad.t + innerH}
        />
        {block.series.map((s) => {
          const pts = block.points
            .filter((p) => typeof p[s.key] === "number")
            .map((p) => `${xScale(p.x)},${yScale(p[s.key])}`)
            .join(" ");
          return (
            <g key={s.key}>
              <polyline
                className="chart-line"
                fill="none"
                stroke={s.color}
                strokeWidth={2.5}
                points={pts}
              />
              {block.points.map((p, i) =>
                typeof p[s.key] === "number" ? (
                  <circle
                    key={i}
                    className="chart-dot"
                    cx={xScale(p.x)}
                    cy={yScale(p[s.key])}
                    r={3.5}
                    fill={s.color}
                  />
                ) : null,
              )}
            </g>
          );
        })}
        {block.points.map((p, i) => (
          <text
            key={i}
            className="chart-tick"
            x={xScale(p.x)}
            y={pad.t + innerH + 16}
            textAnchor="middle"
          >
            {p.x}
          </text>
        ))}
        <text
          className="chart-axis-label"
          x={pad.l + innerW / 2}
          y={H - 4}
          textAnchor="middle"
        >
          {block.xLabel}
        </text>
      </svg>
      <ul className="chart-legend">
        {block.series.map((s) => (
          <li key={s.key}>
            <span className="chart-swatch" style={{ background: s.color }} />
            {s.label}
          </li>
        ))}
      </ul>
    </figure>
  );
}

function parseBarChart(
  viz: Record<string, unknown>,
  pick: PickFn,
): BarChartBlock | null {
  if (viz.kind !== "bar_chart") return null;
  const raw = Array.isArray(viz.bars) ? viz.bars : [];
  const bars = raw
    .map((b, i) => {
      const r = asRecord(b) || {};
      return {
        label: pick(
          String(r.label_vi || r.label || ""),
          String(r.label_en || r.label_vi || r.label || ""),
        ),
        value: Number(r.value) || 0,
        color: CHART_COLORS[i % CHART_COLORS.length],
      };
    })
    .filter((b) => b.label);
  if (!bars.length) return null;
  return {
    title: pick(
      String(viz.title_vi || "Biểu đồ cột"),
      String(viz.title_en || viz.title_vi || "Bar chart"),
    ),
    caption: pick(
      String(viz.caption_vi || ""),
      String(viz.caption_en || viz.caption_vi || ""),
    ),
    yLabel: pick(
      String(viz.y_label_vi || "y"),
      String(viz.y_label_en || viz.y_label_vi || "y"),
    ),
    bars,
  };
}

export function BarChart({ block }: { block: BarChartBlock }) {
  const W = 520;
  const H = 280;
  const pad = { t: 20, r: 16, b: 72, l: 48 };
  const innerW = W - pad.l - pad.r;
  const innerH = H - pad.t - pad.b;
  const maxV = Math.max(...block.bars.map((b) => b.value), 0.001);
  const n = block.bars.length;
  const gap = 8;
  const barW = Math.max(12, (innerW - gap * (n - 1)) / n);
  const yTicks = 4;
  const tickVals = Array.from({ length: yTicks + 1 }, (_, i) =>
    (maxV * i) / yTicks,
  );

  return (
    <figure className="viz-line-chart viz-bar-chart">
      <figcaption>{block.title}</figcaption>
      {block.caption ? (
        <p className="chart-caption muted">{block.caption}</p>
      ) : null}
      <svg
        className="line-chart-svg"
        viewBox={`0 0 ${W} ${H}`}
        role="img"
        aria-label={block.title}
      >
        {tickVals.map((yv, i) => {
          const y = pad.t + innerH - (yv / maxV) * innerH;
          return (
            <g key={i}>
              <line
                className="chart-grid"
                x1={pad.l}
                x2={pad.l + innerW}
                y1={y}
                y2={y}
              />
              <text
                className="chart-tick"
                x={pad.l - 6}
                y={y + 3}
                textAnchor="end"
              >
                {yv >= 10 ? yv.toFixed(0) : yv.toFixed(1)}
              </text>
            </g>
          );
        })}
        <line
          className="chart-axis"
          x1={pad.l}
          y1={pad.t}
          x2={pad.l}
          y2={pad.t + innerH}
        />
        <line
          className="chart-axis"
          x1={pad.l}
          y1={pad.t + innerH}
          x2={pad.l + innerW}
          y2={pad.t + innerH}
        />
        {block.bars.map((b, i) => {
          const h = (b.value / maxV) * innerH;
          const x = pad.l + i * (barW + gap);
          const y = pad.t + innerH - h;
          const short =
            b.label.length > 14 ? `${b.label.slice(0, 12)}…` : b.label;
          return (
            <g key={i}>
              <rect
                className="chart-bar"
                x={x}
                y={y}
                width={barW}
                height={Math.max(h, 1)}
                fill={b.color}
                rx={3}
              >
                <title>{`${b.label}: ${b.value.toFixed(2)} ms`}</title>
              </rect>
              <text
                className="chart-tick"
                x={x + barW / 2}
                y={y - 4}
                textAnchor="middle"
              >
                {b.value >= 10 ? b.value.toFixed(0) : b.value.toFixed(1)}
              </text>
              <text
                className="chart-tick chart-bar-label"
                x={x + barW / 2}
                y={pad.t + innerH + 14}
                textAnchor="end"
                transform={`rotate(-38 ${x + barW / 2} ${pad.t + innerH + 14})`}
              >
                {short}
              </text>
            </g>
          );
        })}
        <text
          className="chart-axis-label"
          x={12}
          y={pad.t + innerH / 2}
          textAnchor="middle"
          transform={`rotate(-90 12 ${pad.t + innerH / 2})`}
        >
          {block.yLabel}
        </text>
      </svg>
    </figure>
  );
}

type ArchNode = {
  id: string;
  label: string;
  role: string;
};

type ArchEdge = {
  from: string;
  to: string;
  label: string;
  bidirectional?: boolean;
};

export type ArchitectureBlock = {
  title: string;
  caption: string;
  nodes: ArchNode[];
  edges: ArchEdge[];
  modules: Record<string, string>;
};

/** Parse architecture from `viz` or embedded `architecture` field. */
export function parseArchitectureFromData(
  data: Record<string, unknown> | null | undefined,
  pick: PickFn,
): ArchitectureBlock | null {
  if (!data) return null;
  const viz = asRecord(data.viz);
  if (viz) {
    const fromViz = parseArchitecture(viz, pick);
    if (fromViz) return fromViz;
  }
  const embedded = asRecord(data.architecture);
  if (embedded) return parseArchitecture(embedded, pick);
  return null;
}

function parseArchitecture(
  viz: Record<string, unknown>,
  pick: PickFn,
): ArchitectureBlock | null {
  if (viz.kind !== "architecture") return null;
  const rawNodes = Array.isArray(viz.nodes) ? viz.nodes : [];
  const nodes: ArchNode[] = rawNodes.map((n) => {
    const r = asRecord(n) || {};
    return {
      id: String(r.id || ""),
      label: pick(String(r.label_vi || ""), String(r.label_en || r.label_vi || "")),
      role: String(r.role || "service"),
    };
  }).filter((n) => n.id);
  if (!nodes.length) return null;
  const edges: ArchEdge[] = (Array.isArray(viz.edges) ? viz.edges : []).map(
    (e) => {
      const r = asRecord(e) || {};
      return {
        from: String(r.from || ""),
        to: String(r.to || ""),
        label: String(r.label || ""),
        bidirectional: Boolean(r.bidirectional),
      };
    },
  );
  const mods = asRecord(viz.modules) || {};
  const modules: Record<string, string> = {};
  for (const [k, v] of Object.entries(mods)) modules[k] = String(v);
  return {
    title: pick(
      String(viz.title_vi || "Sơ đồ kiến trúc hệ thống"),
      String(viz.title_en || viz.title_vi || "System architecture diagram"),
    ),
    caption: pick(
      String(viz.caption_vi || ""),
      String(viz.caption_en || viz.caption_vi || ""),
    ),
    nodes,
    edges,
    modules,
  };
}

export function ArchitectureDiagram({ block }: { block: ArchitectureBlock }) {
  const byId = useMemo(() => {
    const m = new Map<string, ArchNode>();
    for (const n of block.nodes) m.set(n.id, n);
    return m;
  }, [block.nodes]);

  const node = (id: string) => {
    const n = byId.get(id);
    if (!n) return null;
    return (
      <div key={id} className={`arch-node role-${n.role}`}>
        {n.label.split("\n").map((line, i) => (
          <span key={i} className={i === 0 ? "arch-node-main" : "arch-node-sub"}>
            {line}
          </span>
        ))}
      </div>
    );
  };

  const arrow = (label?: string, bi?: boolean) => (
    <div className={`arch-arrow ${bi ? "bi" : ""}`} aria-hidden>
      <span className="arch-arrow-line" />
      {label ? <span className="arch-arrow-label">{label}</span> : null}
      <span className="arch-arrow-head">{bi ? "↔" : "↓"}</span>
    </div>
  );

  const edgeLabel = (from: string, to: string) =>
    block.edges.find((e) => e.from === from && e.to === to)?.label || "";
  const edgeBi = (from: string, to: string) =>
    Boolean(block.edges.find((e) => e.from === from && e.to === to)?.bidirectional);

  const services = ["kg", "vec", "scorer"].filter((id) => byId.has(id));

  return (
    <figure className="viz-architecture">
      <figcaption>{block.title}</figcaption>
      {block.caption ? <p className="arch-caption muted">{block.caption}</p> : null}
      <div className="arch-canvas" role="img" aria-label={block.title}>
        {node("query")}
        {byId.has("query") && byId.has("api") ? arrow(edgeLabel("query", "api")) : null}
        {node("api")}
        {byId.has("api") && byId.has("edgr") ? arrow(edgeLabel("api", "edgr")) : null}
        <div className="arch-mid">
          <div className="arch-core">{node("edgr")}</div>
          {services.length > 0 ? (
            <div className="arch-services">
              <div className="arch-services-link" aria-hidden>
                {edgeBi("edgr", services[0] || "kg") ? "↔" : "→"}
              </div>
              <div className="arch-services-col">
                {services.map((id) => (
                  <div key={id} className="arch-service-wrap">
                    {node(id)}
                    {edgeLabel("edgr", id) ? (
                      <span className="arch-svc-label muted tiny">
                        {edgeLabel("edgr", id)}
                      </span>
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </div>
        {byId.has("edgr") && byId.has("gen") ? arrow(edgeLabel("edgr", "gen")) : null}
        {node("gen")}
        {byId.has("gen") && byId.has("answer")
          ? arrow(edgeLabel("gen", "answer"))
          : null}
        {node("answer")}
      </div>
      {Object.keys(block.modules).length > 0 ? (
        <dl className="arch-modules">
          {Object.entries(block.modules).map(([k, v]) => (
            <div key={k} className="arch-mod-row">
              <dt>{k}</dt>
              <dd>
                <code>{v}</code>
              </dd>
            </div>
          ))}
        </dl>
      ) : null}
    </figure>
  );
}

function parseVizPayload(data: Record<string, unknown>, pick: PickFn) {
  const viz = asRecord(data.viz);
  const blocks: MatrixBlock[] = [];
  let graph: { title: string; nodes: GraphNode[]; edges: GraphEdge[] } | null =
    null;
  let architecture: ArchitectureBlock | null = null;
  const lineCharts: LineChartBlock[] = [];
  const barCharts: BarChartBlock[] = [];

  const pushChart = (r: Record<string, unknown>) => {
    const line = parseLineChart(r, pick);
    if (line && !lineCharts.some((x) => x.title === line.title)) {
      lineCharts.push(line);
    }
    const bar = parseBarChart(r, pick);
    if (bar && !barCharts.some((x) => x.title === bar.title)) {
      barCharts.push(bar);
    }
  };

  if (viz?.kind === "coverage_matrix") {
    const pairLabels = Array.isArray(viz.pair_labels)
      ? (viz.pair_labels as string[])
      : [];
    const pairMatrix = Array.isArray(viz.pair_matrix)
      ? (viz.pair_matrix as number[][])
      : [];
    if (pairLabels.length && pairMatrix.length) {
      blocks.push({
        title: pick(
          "Ma trận đồng xuất hiện chủ đề (Pair)",
          "Topic co-occurrence matrix (Pair)",
        ),
        rowLabels: pairLabels,
        colLabels: pairLabels,
        values: pairMatrix,
      });
    }
    const incRows = Array.isArray(viz.incidence_row_labels)
      ? (viz.incidence_row_labels as string[])
      : [];
    const incCols = Array.isArray(viz.incidence_col_labels)
      ? (viz.incidence_col_labels as string[])
      : [];
    const inc = Array.isArray(viz.incidence_matrix)
      ? (viz.incidence_matrix as number[][])
      : [];
    if (incRows.length && incCols.length && inc.length) {
      blocks.push({
        title: pick(
          "Ma trận incidence paper × topic (0/1)",
          "Paper × topic incidence matrix (0/1)",
        ),
        rowLabels: incRows,
        colLabels: incCols,
        values: inc,
        binary: true,
      });
    }
  }

  if (viz?.kind === "knowledge_graph") {
    const nodes = Array.isArray(viz.nodes) ? (viz.nodes as GraphNode[]) : [];
    const edges = Array.isArray(viz.edges) ? (viz.edges as GraphEdge[]) : [];
    graph = {
      title: pick(
        String(viz.title_vi || "Đồ thị tri thức"),
        String(viz.title_en || viz.title_vi || "Knowledge graph"),
      ),
      nodes,
      edges,
    };
  }

  architecture = parseArchitectureFromData(data, pick);

  if (viz?.kind === "line_chart" || viz?.kind === "bar_chart") {
    pushChart(viz);
  }
  if (viz?.kind === "multi_chart" && Array.isArray(viz.charts)) {
    for (const ch of viz.charts) {
      const r = asRecord(ch);
      if (r) pushChart(r);
    }
  }
  if (Array.isArray(data.charts)) {
    for (const ch of data.charts) {
      const r = asRecord(ch);
      if (r) pushChart(r);
    }
  }
  // Fallback: stage timings → bar chart for Analyze(time)
  if (
    !barCharts.length &&
    Array.isArray(data.empirical_stages_ms) &&
    data.empirical_stages_ms.length > 0
  ) {
    const c = parseBarChart(
      {
        kind: "bar_chart",
        title_vi: "Phân bổ thời gian theo giai đoạn EDGR",
        title_en: "EDGR stage time breakdown",
        y_label_vi: "Thời gian (ms)",
        y_label_en: "Time (ms)",
        bars: (data.empirical_stages_ms as Array<Record<string, unknown>>).map(
          (s) => ({
            label_vi: `φ${s.stage} ${s.name ?? ""}`,
            label_en: `φ${s.stage} ${s.name ?? ""}`,
            value: s.duration_ms,
          }),
        ),
      },
      pick,
    );
    if (c) barCharts.push(c);
  }
  if (
    !lineCharts.some((c) => c.title.toLowerCase().includes("latency")) &&
    Array.isArray(data.latency_by_top_k) &&
    data.latency_by_top_k.length > 0
  ) {
    const c = parseLineChart(
      {
        kind: "line_chart",
        title_vi: "Độ phức tạp thời gian thực nghiệm (latency theo top_k)",
        title_en: "Empirical time complexity (latency vs top_k)",
        x_label_vi: "top_k",
        x_label_en: "top_k",
        points: (data.latency_by_top_k as Array<Record<string, unknown>>).map(
          (r) => ({
            x: r.top_k,
            latency_ms: r.latency_ms,
          }),
        ),
        series: [
          {
            key: "latency_ms",
            label_vi: "Latency (ms)",
            label_en: "Latency (ms)",
          },
        ],
      },
      pick,
    );
    if (c) lineCharts.push(c);
  }
  // Fallback: convergence series table → chart
  if (
    !lineCharts.length &&
    Array.isArray(data.series) &&
    data.series.length > 0
  ) {
    const rows = data.series as Array<Record<string, unknown>>;
    if (rows[0] && ("prefix_stability" in rows[0] || "top_k" in rows[0])) {
      const c = parseLineChart(
        {
          kind: "line_chart",
          title_vi: "Biểu đồ hội tụ thực nghiệm (theo top-k)",
          title_en: "Empirical convergence chart (vs top-k)",
          caption_vi:
            "prefix_stability và faithfulness khi tăng top_k — hội tụ khi đường ổn định.",
          caption_en:
            "prefix_stability and faithfulness as top_k grows — convergence when curves stabilize.",
          x_label_vi: "top_k",
          x_label_en: "top_k",
          points: rows.map((r) => ({
            x: Number(r.top_k) || 0,
            prefix_stability: Number(r.prefix_stability) || 0,
            faithfulness: Number(r.faithfulness) || 0,
          })),
          series: [
            {
              key: "prefix_stability",
              label_vi: "Prefix stability",
              label_en: "Prefix stability",
            },
            {
              key: "faithfulness",
              label_vi: "Faithfulness",
              label_en: "Faithfulness",
            },
          ],
        },
        pick,
      );
      if (c) lineCharts.push(c);
    }
  }
  // Fallback: scalability scale_rows → chart
  if (
    !lineCharts.length &&
    Array.isArray(data.scale_rows) &&
    data.scale_rows.length > 0
  ) {
    const rows = data.scale_rows as Array<Record<string, unknown>>;
    const c = parseLineChart(
      {
        kind: "line_chart",
        title_vi: "Biểu đồ khả năng mở rộng (latency theo |D|)",
        title_en: "Scalability chart (latency vs |D|)",
        x_label_vi: "|D|",
        x_label_en: "|D|",
        points: rows.map((r) => ({
          x: Number(r.evidence_corpus_size) || 0,
          latency_ms: Number(r.latency_ms) || 0,
        })),
        series: [
          { key: "latency_ms", label_vi: "Latency (ms)", label_en: "Latency (ms)" },
        ],
      },
      pick,
    );
    if (c) lineCharts.push(c);
  }

  if (
    !blocks.length &&
    Array.isArray(data.pair_matrix) &&
    Array.isArray(data.topics)
  ) {
    const topics = data.topics as string[];
    blocks.push({
      title: pick(
        "Ma trận đồng xuất hiện chủ đề (Pair)",
        "Topic co-occurrence matrix (Pair)",
      ),
      rowLabels: topics,
      colLabels: topics,
      values: data.pair_matrix as number[][],
    });
  }

  if (
    !graph &&
    Array.isArray(data.extracted_nodes) &&
    (data.extracted_nodes as unknown[]).length > 0
  ) {
    const nodes = (data.extracted_nodes as Array<Record<string, unknown>>).map(
      (n) => ({
        id: String(n.id),
        label: String(n.label ?? n.id),
        type: String(n.type ?? "entity"),
        seed: Boolean(n.hop === 0),
      }),
    );
    graph = {
      title: pick("Đồ thị trích xuất", "Extracted graph"),
      nodes,
      edges: [],
    };
  }

  return { blocks, graph, architecture, lineCharts, barCharts };
}

export function hasResultViz(data: unknown): boolean {
  const obj = asRecord(data);
  if (!obj) return false;
  const viz = asRecord(obj.viz);
  if (
    viz?.kind === "coverage_matrix" ||
    viz?.kind === "knowledge_graph" ||
    viz?.kind === "architecture" ||
    viz?.kind === "line_chart" ||
    viz?.kind === "bar_chart" ||
    viz?.kind === "multi_chart"
  ) {
    return true;
  }
  const embedded = asRecord(obj.architecture);
  if (embedded?.kind === "architecture") return true;
  if (Array.isArray(obj.charts) && obj.charts.length > 0) return true;
  if (Array.isArray(obj.series) && obj.series.length > 0) {
    const row0 = asRecord(obj.series[0]);
    if (row0 && ("prefix_stability" in row0 || "top_k" in row0)) return true;
  }
  if (
    Array.isArray(obj.empirical_stages_ms) &&
    obj.empirical_stages_ms.length > 0
  ) {
    return true;
  }
  if (
    Array.isArray(obj.latency_by_top_k) &&
    obj.latency_by_top_k.length > 0
  ) {
    return true;
  }
  if (Array.isArray(obj.scale_rows) && obj.scale_rows.length > 0) return true;
  if (Array.isArray(obj.pair_matrix) && Array.isArray(obj.topics)) return true;
  if (Array.isArray(obj.extracted_nodes) && obj.extracted_nodes.length > 0) {
    return true;
  }
  return false;
}

export function ResultDataViz({ data }: { data: unknown }) {
  const { pick } = useLocale();
  const obj = asRecord(data);
  if (!obj) return null;
  const parsed = parseVizPayload(obj, pick);
  if (
    !parsed.blocks.length &&
    !parsed.graph &&
    !parsed.architecture &&
    !parsed.lineCharts.length &&
    !parsed.barCharts.length
  ) {
    return null;
  }

  const matrices = parsed.blocks;
  // Pair + incidence: one row, two columns (Step 1 coverage matrix).
  const pairRow =
    matrices.length >= 2 ? (
      <div className="viz-matrix-row" key="pair-incidence-row">
        <MatrixHeatmap block={matrices[0]} />
        <MatrixHeatmap block={matrices[1]} />
      </div>
    ) : null;
  const restMatrices =
    matrices.length >= 2
      ? matrices.slice(2)
      : matrices.length === 1
        ? matrices
        : [];

  const timePair =
    parsed.barCharts.length >= 1 && parsed.lineCharts.length >= 1 ? (
      <div className="viz-chart-row" key="time-charts-row">
        <BarChart key={parsed.barCharts[0].title} block={parsed.barCharts[0]} />
        <LineChart key={parsed.lineCharts[0].title} block={parsed.lineCharts[0]} />
      </div>
    ) : null;

  const chartRow =
    !timePair && parsed.lineCharts.length >= 2 ? (
      <div className="viz-chart-row" key="line-charts-row">
        {parsed.lineCharts.map((c) => (
          <LineChart key={c.title} block={c} />
        ))}
      </div>
    ) : null;

  return (
    <div className="result-viz stack">
      {parsed.architecture ? (
        <ArchitectureDiagram block={parsed.architecture} />
      ) : null}
      {timePair}
      {chartRow}
      {!timePair && !chartRow
        ? parsed.lineCharts.map((c) => <LineChart key={c.title} block={c} />)
        : null}
      {!timePair
        ? parsed.barCharts.map((c) => <BarChart key={c.title} block={c} />)
        : parsed.barCharts.slice(1).map((c) => (
            <BarChart key={c.title} block={c} />
          ))}
      {!timePair
        ? null
        : parsed.lineCharts.slice(1).map((c) => (
            <LineChart key={c.title} block={c} />
          ))}
      {pairRow}
      {restMatrices.map((b) => (
        <MatrixHeatmap key={b.title} block={b} />
      ))}
      {parsed.graph ? (
        <GraphNetwork
          title={parsed.graph.title}
          nodes={parsed.graph.nodes}
          edges={parsed.graph.edges}
        />
      ) : null}
    </div>
  );
}
