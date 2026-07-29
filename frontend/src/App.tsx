import {
  useEffect,
  useMemo,
  useState,
  type CSSProperties,
  type ReactNode,
} from "react";
import {
  api,
  type AcademicPackage,
  type PipelineDefinition,
  type PipelineStep,
  type ResultReview,
  type TableGuide,
  type TaskResult,
} from "./api";
import { AcademicPanel } from "./AcademicPanel";
import { hasResultViz, ResultDataViz, VIZ_CONSUMED_KEYS } from "./DataViz";
import { LanguageMenu } from "./i18n/LanguageMenu";
import { useLocale } from "./i18n/LocaleContext";
import { downloadCsv, csvFilename } from "./downloadCsv";
import {
  AssessmentView,
  PublicationManuscriptView,
  PublicationPlanView,
} from "./modelViews";
import { Formula, looksLikeFormula } from "./mathFormat";
import { IdsCtiApp } from "./IdsCtiApp";
import { OverviewTab } from "./OverviewTab";
import { STEP_COLORS, StepIcon, TaskIcon } from "./StepIcon";
import { StepRail } from "./StepRail";
import "./index.css";

const SAMPLE_QUERIES = [
  "What is CVE-2021-44228 and how is it exploited?",
  "Which ATT&CK techniques does APT29 commonly use?",
  "How can NIDS detect lateral movement?",
  "Which CVE did Cl0p exploit in MOVEit campaigns?",
  "How does EDGR reduce hallucination in CTI answers?",
];

/** Research default for IDS/CTI + EDGR (matches backend DEFAULT_TOP_K). */
const DEFAULT_TOP_K = 5;
const TOP_K_CHOICES = [3, 5, 8] as const;

/** First child slot under each parent step = step overview (not a runnable task). */
const STEP_OVERVIEW = "__overview__";

function ScientificVerifyPanel({
  verification,
  onJumpHumanEval,
}: {
  verification?: ResultReview["scientific_verification"];
  onJumpHumanEval?: () => void;
}) {
  const { t, pick } = useLocale();
  if (!verification) return null;
  const status = verification.runtime_status ?? "pending";
  const statusLabel = pick(
    verification.runtime_status_vi ?? "",
    verification.runtime_status_en ?? "",
  );
  const protocol = pick(
    verification.protocol_vi ?? "",
    verification.protocol_en ?? "",
  );
  const expert = verification.expert;
  const expertLabel = expert
    ? pick(expert.status_vi ?? "", expert.status_en ?? "")
    : "";
  const checks = verification.checks ?? [];
  const badgeKey =
    status === "verified"
      ? "sci_verify_badge_verified"
      : status === "partial"
        ? "sci_verify_badge_partial"
        : status === "weak"
          ? "sci_verify_badge_weak"
          : "sci_verify_badge_pending";

  return (
    <div className={`review-block sci-verify status-${status}`}>
      <div className="sci-verify-head">
        <h4>{t("sci_verify_h")}</h4>
        <span className={`sci-verify-badge ${status}`}>{t(badgeKey)}</span>
      </div>
      {statusLabel ? <p className="sci-verify-status">{statusLabel}</p> : null}
      {protocol ? (
        <p className="muted tiny">
          <strong>{t("sci_verify_protocol")}: </strong>
          {protocol}
        </p>
      ) : null}
      {checks.length > 0 ? (
        <ul className="sci-verify-checks">
          {checks.map((c) => (
            <li key={c.id} className={c.ok ? "ok" : "fail"}>
              <span className="sci-verify-mark" aria-hidden>
                {c.ok ? "✓" : "✗"}
              </span>
              <div>
                <strong>
                  {pick(c.title_vi ?? "", c.title_en ?? c.title_vi ?? "")}
                </strong>
                <p className="muted tiny">
                  {pick(c.detail_vi ?? "", c.detail_en ?? c.detail_vi ?? "")}
                </p>
              </div>
              <span className="sci-verify-pill">
                {c.ok ? t("sci_verify_pass") : t("sci_verify_fail")}
              </span>
            </li>
          ))}
        </ul>
      ) : null}
      {expert ? (
        <div className="sci-verify-expert">
          <strong>{t("sci_verify_expert")}</strong>
          <p>{expertLabel}</p>
          {typeof expert.kappa === "number" ? (
            <p className="muted tiny">
              κ = {expert.kappa.toFixed(2)} · n_dual = {expert.n_dual ?? 0}
            </p>
          ) : null}
          {onJumpHumanEval ? (
            <button
              type="button"
              className="table-dl-btn sci-verify-jump"
              onClick={onJumpHumanEval}
            >
              {t("sci_verify_jump_he")}
            </button>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

function ResultReviewPanel({
  review,
  onJumpHumanEval,
}: {
  review?: ResultReview;
  onJumpHumanEval?: () => void;
}) {
  const { t, pick } = useLocale();
  if (!review) return null;
  const bullets = pick(review.bullets_vi ?? [], review.bullets_en ?? []);
  const explain = pick(review.explain_vi ?? "", review.explain_en ?? "");
  const how = pick(review.how_to_read_vi ?? "", review.how_to_read_en ?? "");
  const ev = review.evidence;
  const evClaim = ev
    ? pick(ev.claim_vi ?? "", ev.claim_en ?? "")
    : "";
  const scalars = ev?.scalars ? Object.entries(ev.scalars) : [];
  const collections = ev?.collections ?? [];

  return (
    <div className="result-review scientific-review">
      <ScientificVerifyPanel
        verification={review.scientific_verification}
        onJumpHumanEval={onJumpHumanEval}
      />

      <div className="review-block">
        <h4>{t("result_explain_h")}</h4>
        {bullets.length > 0 ? (
          <ul>
            {bullets.map((b, i) => (
              <li key={i}>{b}</li>
            ))}
          </ul>
        ) : (
          <p>{explain}</p>
        )}
      </div>

      {(evClaim || scalars.length > 0 || collections.length > 0) && (
        <div className="review-block evidence">
          <h4>{t("result_evidence_h")}</h4>
          {evClaim ? <p className="evidence-claim-line">{evClaim}</p> : null}
          {scalars.length > 0 ? (
            <div className="evidence-stats">
              {scalars.map(([k, v]) => (
                <div key={k} className="stat-chip">
                  <span>{k}</span>
                  <strong>{cellText(v, k)}</strong>
                </div>
              ))}
            </div>
          ) : null}
          {collections.length > 0 ? (
            <p className="muted tiny">
              {collections.map((c) => `${c.field}(n=${c.count})`).join(" · ")}
            </p>
          ) : null}
        </div>
      )}

      {how ? (
        <div className="review-block">
          <h4>{t("result_how_h")}</h4>
          <p>{how}</p>
        </div>
      ) : null}

      {review.assessment ? (
        <div className="review-block assess">
          <h4>{t("result_assess_runtime_h")}</h4>
          <AssessmentView data={review.assessment} />
        </div>
      ) : null}
    </div>
  );
}

/** Fields that are 0–1 ratios → display as percent. */
const RATIO_FIELD =
  /^(faithfulness|hallucination_rate|confidence|p_at_k|r_at_k|mrr|f1|precision|recall|accuracy|score|score_0_1|reliability|freshness|graph_consistency|semantic_relevance|ent_hit|prefix_stability|delta_faithfulness|delta_hallucination)$/i;

/** Fields already stored as 0–100 percent. */
const PERCENT_FIELD = /^(percent|.*_percent|cpu_percent|system_cpu_percent|system_memory_percent)$/i;

function formatMetric(key: string | undefined, v: unknown): string {
  if (typeof v !== "number" || Number.isNaN(v) || !key) return "";
  if (PERCENT_FIELD.test(key)) {
    return `${v % 1 === 0 ? v.toFixed(0) : v.toFixed(1)}%`;
  }
  if (RATIO_FIELD.test(key) && Math.abs(v) <= 1.0001) {
    return `${(v * 100).toFixed(1)}%`;
  }
  // Heuristic: unnamed 0–1 floats in metric-like contexts stay as-is unless key hints rate
  if (/(rate|ratio|score)$/i.test(key) && Math.abs(v) <= 1.0001) {
    return `${(v * 100).toFixed(1)}%`;
  }
  return "";
}

function cellText(v: unknown, key?: string): string {
  if (v == null) return "";
  if (typeof v === "number") {
    const pct = formatMetric(key, v);
    if (pct) return pct;
    if (Number.isInteger(v)) return String(v);
    return Math.abs(v) >= 100 ? v.toFixed(1) : v.toFixed(4).replace(/\.?0+$/, "");
  }
  if (typeof v === "string" || typeof v === "boolean") {
    return String(v);
  }
  if (Array.isArray(v)) {
    if (v.every((x) => typeof x !== "object" || x == null)) {
      return v.map((x) => String(x ?? "")).join(", ");
    }
    return `[${v.length}]`;
  }
  if (typeof v === "object") {
    const o = v as Record<string, unknown>;
    if (typeof o.id === "string" || typeof o.id === "number") {
      return String(o.id);
    }
    try {
      const s = JSON.stringify(v);
      return s.length > 120 ? `${s.slice(0, 117)}…` : s;
    } catch {
      return "[object]";
    }
  }
  return String(v);
}

function collectTableKeys(rows: Record<string, unknown>[], maxCols = 10): string[] {
  const preferred = [
    "id",
    "method",
    "variant",
    "authors",
    "year",
    "title",
    "venue",
    "apa",
    "doi",
    "tags",
    "catalog",
    "synthetic",
    "citable",
    "faithfulness",
    "hallucination_rate",
    "confidence",
    "latency_ms",
    "p_at_k",
    "mrr",
    "f1",
    "precision",
    "recall",
    "score",
    "paper_id",
    "limitation",
    "text",
    "source",
    "severity",
    "statement",
    "name",
    "family",
    "ready",
    "item",
    "step",
    "probe",
  ];
  const seen = new Set<string>();
  const keys: string[] = [];
  for (const k of preferred) {
    if (rows.some((r) => k in r) && !seen.has(k)) {
      seen.add(k);
      keys.push(k);
    }
  }
  for (const r of rows.slice(0, 20)) {
    for (const k of Object.keys(r)) {
      if (seen.has(k)) continue;
      if (k === "apa_parts" || k === "metadata" || k === "stages") continue;
      seen.add(k);
      keys.push(k);
      if (keys.length >= maxCols) return keys;
    }
  }
  return keys.slice(0, maxCols);
}

function TableFrame({
  guide,
  caption,
  children,
  onDownload,
}: {
  guide?: TableGuide | null;
  caption?: string;
  children: ReactNode;
  onDownload?: () => void;
}) {
  const { t, pick } = useLocale();
  const title = guide
    ? pick(guide.title_vi ?? caption ?? "", guide.title_en ?? caption ?? "")
    : caption;
  const explain = guide
    ? pick(guide.explain_vi ?? "", guide.explain_en ?? "")
    : "";
  const evaluate = guide
    ? pick(guide.evaluate_vi ?? "", guide.evaluate_en ?? "")
    : "";
  const verdict = guide
    ? pick(guide.verdict_vi ?? "", guide.verdict_en ?? "")
    : "";

  return (
    <div className="table-block framed">
      <div className="table-head-row">
        {title ? <h5 className="table-caption">{title}</h5> : <span />}
        {onDownload ? (
          <button
            type="button"
            className="table-dl-btn"
            onClick={onDownload}
            title={t("table_download")}
          >
            {t("table_download")}
          </button>
        ) : null}
      </div>
      {explain ? (
        <div className="table-guide">
          <strong>{t("table_explain_h")}</strong>
          <p>{explain}</p>
        </div>
      ) : null}
      {children}
      {(evaluate || verdict) && (
        <div className="table-assess">
          {evaluate ? (
            <p>
              <strong>{t("table_evaluate_h")}: </strong>
              {evaluate}
            </p>
          ) : null}
          {verdict ? (
            <p>
              <strong>{t("table_verdict_h")}: </strong>
              {verdict}
            </p>
          ) : null}
        </div>
      )}
    </div>
  );
}

function CellValue({ value, colKey }: { value: unknown; colKey: string }) {
  const text = cellText(value, colKey);
  if (
    typeof value === "string" &&
    text.length > 0 &&
    text.length < 160 &&
    (/(formula|asymptotic|complexity|latex)/i.test(colKey) ||
      looksLikeFormula(text))
  ) {
    return <Formula expr={text} display={false} />;
  }
  return <>{text}</>;
}

function DataTable({
  rows,
  caption,
  guide,
  pageSize = 60,
}: {
  rows: Record<string, unknown>[];
  caption?: string;
  guide?: TableGuide | null;
  /** Cap DOM rows — large APA catalogs were freezing the tab. */
  pageSize?: number;
}) {
  const [page, setPage] = useState(0);
  if (rows.length === 0) return <p className="muted">[]</p>;
  const keys = collectTableKeys(rows);
  const exportKeys = collectTableKeys(rows, 40);
  const title = caption ?? `${rows.length} rows`;
  const pageCount = Math.max(1, Math.ceil(rows.length / pageSize));
  const safePage = Math.min(page, pageCount - 1);
  const slice = rows.slice(safePage * pageSize, safePage * pageSize + pageSize);
  const onDownload = () => {
    downloadCsv(
      csvFilename(title, "table"),
      ["#", ...exportKeys],
      rows.map((row, i) => [
        i + 1,
        ...exportKeys.map((k) => cellText(row[k], k)),
      ]),
    );
  };
  return (
    <TableFrame guide={guide} caption={title} onDownload={onDownload}>
      {rows.length > pageSize ? (
        <div className="table-pager muted tiny">
          <span>
            {safePage * pageSize + 1}–{Math.min(rows.length, (safePage + 1) * pageSize)} /{" "}
            {rows.length}
          </span>
          <button
            type="button"
            className="table-dl-btn"
            disabled={safePage <= 0}
            onClick={() => setPage((p) => Math.max(0, p - 1))}
          >
            ←
          </button>
          <button
            type="button"
            className="table-dl-btn"
            disabled={safePage >= pageCount - 1}
            onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))}
          >
            →
          </button>
        </div>
      ) : null}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              {keys.map((k) => (
                <th key={k}>{k}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {slice.map((row, i) => {
              const abs = safePage * pageSize + i;
              return (
              <tr key={String(row.id ?? abs)}>
                <td className="mono">{abs + 1}</td>
                {keys.map((k) => (
                  <td key={k} title={cellText(row[k], k)}>
                    {k === "doi" &&
                    typeof row.doi_url === "string" &&
                    row.doi_url ? (
                      <a href={String(row.doi_url)} target="_blank" rel="noreferrer">
                        {cellText(row[k], k)}
                      </a>
                    ) : (
                      <CellValue value={row[k]} colKey={k} />
                    )}
                  </td>
                ))}
              </tr>
            );
            })}
          </tbody>
        </table>
      </div>
    </TableFrame>
  );
}

function ScalarTable({
  entries,
  caption,
  guide,
}: {
  entries: [string, unknown][];
  caption?: string;
  guide?: TableGuide | null;
}) {
  if (entries.length === 0) return null;
  const onDownload = () => {
    downloadCsv(
      csvFilename(caption, "scalars"),
      ["field", "value"],
      entries.map(([k, v]) => [k, cellText(v, k)]),
    );
  };
  return (
    <TableFrame guide={guide} caption={caption} onDownload={onDownload}>
      <div className="table-wrap compact">
        <table>
          <thead>
            <tr>
              <th>field</th>
              <th>value</th>
            </tr>
          </thead>
          <tbody>
            {entries.map(([k, v]) => (
              <tr key={k}>
                <td className="mono">{k}</td>
                <td>
                  <CellValue value={v} colKey={k} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </TableFrame>
  );
}

function ResultView({
  data,
  tableGuides,
}: {
  data: unknown;
  tableGuides?: Record<string, TableGuide> | null;
}) {
  const { t, pick } = useLocale();
  const guides = tableGuides ?? {};
  if (data == null) return <p className="muted">{t("no_result")}</p>;

  if (typeof data === "string" || typeof data === "number" || typeof data === "boolean") {
    return <pre className="result-block">{String(data)}</pre>;
  }

  if (Array.isArray(data)) {
    if (data.length === 0) return <p className="muted">[]</p>;
    if (
      typeof data[0] === "object" &&
      data[0] !== null &&
      !Array.isArray(data[0])
    ) {
      return (
        <DataTable
          rows={data as Record<string, unknown>[]}
          caption={`${t("result_table_h")} (${data.length})`}
        />
      );
    }
    // array of primitives → single-column table
    if (data.every((x) => typeof x !== "object" || x == null)) {
      return (
        <DataTable
          rows={data.map((v, i) => ({ index: i + 1, value: v }))}
          caption={t("result_table_h")}
        />
      );
    }
    return (
      <div className="stack">
        {data.map((item, i) => (
          <div key={i} className="nested-card">
            <ResultView data={item} />
          </div>
        ))}
      </div>
    );
  }

  const obj = data as Record<string, unknown>;
  const showViz = hasResultViz(obj);
  const entries = Object.entries(obj).filter(
    ([k]) => !(showViz && VIZ_CONSUMED_KEYS.has(k)),
  );

  // Special: matrix / knowledge-graph / architecture figures (not only tables)
  if (showViz) {
    const rest: Record<string, unknown> = {};
    for (const [k, v] of entries) rest[k] = v;
    // Architecture / charts already drawn — avoid dumping raw companions again.
    const viz = obj.viz as Record<string, unknown> | undefined;
    if (viz?.kind === "architecture") {
      delete rest.flow;
      delete rest.modules;
    }
    if (
      viz?.kind === "line_chart" ||
      viz?.kind === "bar_chart" ||
      viz?.kind === "multi_chart"
    ) {
      delete rest.charts;
    }
    return (
      <div className="stack">
        <ResultDataViz data={obj} />
        {Object.keys(rest).length > 0 ? (
          <ResultView data={rest} tableGuides={guides} />
        ) : null}
      </div>
    );
  }

  // Special: Step-1 bibliography catalog (≥300 refs) — APA table
  if (Array.isArray(obj.catalog) && typeof obj.total === "number") {
    const note = pick(
      String(obj.note_vi ?? ""),
      String(obj.note_en ?? obj.note_vi ?? ""),
    );
    const rows = (obj.catalog as Array<Record<string, unknown>>).map((r) => ({
      id: r.id,
      authors: (r.apa_parts as Record<string, string> | undefined)?.authors ?? r.authors,
      year: r.year,
      title: (r.apa_parts as Record<string, string> | undefined)?.title ?? r.title,
      venue: r.venue,
      apa: r.apa,
      doi: r.doi,
      doi_url: r.doi_url,
      tags: r.tags,
      catalog: r.catalog,
      synthetic: r.synthetic,
      citable: r.citable,
    }));
    const meta: Record<string, unknown> = {};
    if (obj.by_tag) meta.by_tag = obj.by_tag;
    if (obj.year_span) meta.year_span = obj.year_span;
    if (obj.filter) meta.filter = obj.filter;
    return (
      <div className="stack apa-catalog">
        {note ? <p className="catalog-note">{note}</p> : null}
        <ScalarTable
          caption={t("result_scalars_h")}
          guide={guides._scalars}
          entries={[
            ["total", obj.total],
            ["core", obj.core_count],
            ["extended", obj.extended_count],
            ["style", obj.style ?? "APA 7th"],
          ].filter(([, v]) => v != null) as [string, unknown][]}
        />
        <DataTable
          rows={rows}
          caption={`${t("apa_h")} (${rows.length})`}
          guide={guides.catalog}
        />
        {Object.keys(meta).length > 0 ? (
          <details className="catalog-meta">
            <summary>{t("apa_meta")}</summary>
            <ResultView data={meta} tableGuides={guides} />
          </details>
        ) : null}
      </div>
    );
  }

  // Special: answer string prominent + rest as tables
  if (typeof obj.answer === "string") {
    const { answer, ...rest } = obj;
    return (
      <div className="stack">
        <div className="answer">{answer}</div>
        {Object.keys(rest).length > 0 && (
          <ResultView data={rest} tableGuides={guides} />
        )}
      </div>
    );
  }

  // Step-13 manuscripts: full draft is in AcademicPanel (Operating model).
  // After Run, Results must NOT repeat the entire manuscript — only live artifacts.
  if (
    obj.kind === "publication_manuscript" ||
    (Array.isArray(obj.sections) &&
      obj.sections.length > 0 &&
      (typeof obj.working_title === "string" ||
        typeof obj.contribution_claim_vi === "string"))
  ) {
    const live =
      obj.live_artifacts &&
      typeof obj.live_artifacts === "object" &&
      !Array.isArray(obj.live_artifacts)
        ? (obj.live_artifacts as Record<string, unknown>)
        : null;
    if (live && Object.keys(live).length > 0) {
      return (
        <div className="stack pub-live-only">
          <p className="muted tiny">
            {pick(
              "Outline manuscript nằm ở «Mô hình hoạt động» phía trên. Đây chỉ là live_artifacts sau khi Chạy.",
              "The manuscript outline is in the Operating model above. This block is live_artifacts after Run only.",
            )}
          </p>
          <ResultView data={live} tableGuides={guides} />
        </div>
      );
    }
    return <PublicationManuscriptView data={obj} />;
  }

  // Step-14 chapter outline (not full prose)
  if (
    obj.kind === "chapter_outline" ||
    (Array.isArray(obj.outline) && obj.draft_notes != null && obj.ch != null)
  ) {
    const note = pick(
      String(obj.draft_notes ?? ""),
      String(obj.draft_notes_en ?? obj.draft_notes ?? ""),
    );
    const sections = Array.isArray(obj.sections)
      ? (obj.sections as Array<Record<string, unknown>>)
      : [];
    const rest = { ...obj };
    delete rest.kind;
    delete rest.draft_notes;
    delete rest.draft_notes_en;
    delete rest.sections;
    return (
      <div className="stack">
        <p className="muted tiny result-honesty">{t("chapter_outline_note")}</p>
        {note ? <p className="result-chapter-note">{note}</p> : null}
        {sections.length > 0 ? (
          <div className="chapter-sections">
            {sections.map((sec, i) => (
              <article key={i} className="chapter-section surface">
                <strong>{String(sec.heading ?? `§${i + 1}`)}</strong>
                <p>
                  {pick(
                    String(sec.prose_vi ?? ""),
                    String(sec.prose_en ?? sec.prose_vi ?? ""),
                  )}
                </p>
              </article>
            ))}
          </div>
        ) : null}
        <ResultView data={rest} tableGuides={guides} />
      </div>
    );
  }

  // Step-7 seed replay honesty
  if (obj.mode === "seed_replay" || obj.mode === "seed_inventory") {
    const note = pick(
      String(obj.note_vi ?? ""),
      String(obj.note_en ?? obj.note ?? ""),
    );
    const rest = { ...obj };
    delete rest.mode;
    delete rest.note_vi;
    delete rest.note_en;
    delete rest.note;
    return (
      <div className="stack">
        <p className="muted tiny result-honesty">
          {pick(
            "Seed replay trên corpus demo — không phải crawl API live. Báo cáo before/after + normalize_ops.",
            "Seed replay on the demo corpus — not a live API crawl. Shows before/after + normalize_ops.",
          )}
        </p>
        {note ? <p className="muted tiny">{note}</p> : null}
        <ResultView data={rest} tableGuides={guides} />
      </div>
    );
  }

  // Step-9 baseline honesty badge
  if (
    typeof obj.implementation === "string" &&
    String(obj.implementation).includes("stub")
  ) {
    const policy = Array.isArray(obj.policy_steps)
      ? (obj.policy_steps as string[])
      : [];
    const noteTxt = pick(
      String(obj.note_vi ?? ""),
      String(obj.note_en ?? obj.note ?? ""),
    );
    const rest = { ...obj };
    delete rest.implementation;
    delete rest.note;
    delete rest.note_vi;
    delete rest.note_en;
    delete rest.policy_steps;
    return (
      <div className="stack">
        <p className="muted tiny result-honesty">
          {t("stub_baseline_note")}
          <span className="mono"> · {String(obj.implementation)}</span>
        </p>
        {policy.length > 0 ? (
          <ol className="policy-steps">
            {policy.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ol>
        ) : null}
        {noteTxt ? <p className="muted tiny">{noteTxt}</p> : null}
        <ResultView data={rest} tableGuides={guides} />
      </div>
    );
  }
  if (
    Array.isArray(obj.results) &&
    typeof obj.note === "string" &&
    /stub/i.test(String(obj.note))
  ) {
    const { note, ...rest } = obj;
    return (
      <div className="stack">
        <p className="muted tiny result-honesty">{t("stub_baseline_note")}</p>
        {note ? <p className="muted tiny">{String(note)}</p> : null}
        <ResultView data={rest} tableGuides={guides} />
      </div>
    );
  }
  if (
    obj.kind === "publication_plan" ||
    ((typeof obj.strategy_vi === "string" || typeof obj.strategy_en === "string") &&
      Array.isArray(obj.timeline_hint))
  ) {
    // Plan outline is already in AcademicPanel ops; after Run show paper snapshot table only.
    if (Array.isArray(obj.papers) && obj.papers.length > 0) {
      return (
        <div className="stack">
          <p className="muted tiny">
            {pick(
              "Chiến lược/timeline đầy đủ nằm ở «Mô hình hoạt động» phía trên. Bên dưới: snapshot 4 bài sau Chạy.",
              "Full strategy/timeline is in the Operating model above. Below: 4-paper snapshot after Run.",
            )}
          </p>
          <DataTable
            rows={obj.papers as Record<string, unknown>[]}
            caption={pick("Snapshot 4 bài báo", "4-paper snapshot")}
          />
        </div>
      );
    }
    return <PublicationPlanView data={obj} />;
  }

  // Topic-survey runtime
  if (
    typeof obj.topic === "string" &&
    typeof obj.paper_count === "number" &&
    Array.isArray(obj.papers)
  ) {
    return (
      <div className="stack">
        <ScalarTable
          caption={`${String(obj.topic)} — ${t("result_scalars_h")}`}
          guide={guides._scalars}
          entries={[
            ["topic", obj.topic],
            ["scope", obj.scope],
            ["paper_count", obj.paper_count],
            ["limitation_count", obj.limitation_count],
            ["scaffold_excluded", obj.scaffold_count_excluded],
          ].filter(([, v]) => v != null) as [string, unknown][]}
        />
        <DataTable
          rows={obj.papers as Record<string, unknown>[]}
          caption={`papers (${(obj.papers as unknown[]).length})`}
          guide={guides.papers}
        />
        {Array.isArray(obj.limitations) && obj.limitations.length > 0 ? (
          <DataTable
            rows={obj.limitations as Record<string, unknown>[]}
            caption={`limitations (${obj.limitations.length})`}
            guide={guides.limitations}
          />
        ) : null}
      </div>
    );
  }

  // Generic object: scalars as 2-col table; each array-of-objects as its own table
  const scalars: [string, unknown][] = [];
  const tables: Array<{ key: string; rows: Record<string, unknown>[] }> = [];
  const nested: [string, unknown][] = [];

  for (const [k, v] of entries) {
    if (v == null) continue;
    if (typeof v === "string" || typeof v === "number" || typeof v === "boolean") {
      scalars.push([k, v]);
      continue;
    }
    if (
      Array.isArray(v) &&
      v.length > 0 &&
      typeof v[0] === "object" &&
      v[0] !== null &&
      !Array.isArray(v[0])
    ) {
      tables.push({ key: k, rows: v as Record<string, unknown>[] });
      continue;
    }
    if (Array.isArray(v) && v.every((x) => typeof x !== "object" || x == null)) {
      tables.push({
        key: k,
        rows: v.map((item, i) => ({ index: i + 1, value: item })),
      });
      continue;
    }
    if (typeof v === "object" && !Array.isArray(v)) {
      const inner = v as Record<string, unknown>;
      const innerEntries = Object.entries(inner);
      if (
        innerEntries.length > 0 &&
        innerEntries.every(
          ([, iv]) =>
            iv == null ||
            typeof iv === "string" ||
            typeof iv === "number" ||
            typeof iv === "boolean",
        )
      ) {
        tables.push({
          key: k,
          rows: innerEntries.map(([ik, iv]) => ({ key: ik, value: iv })),
        });
        continue;
      }
    }
    nested.push([k, v]);
  }

  if (scalars.length === 0 && tables.length === 0 && nested.length === 0) {
    return <p className="muted">{t("no_result")}</p>;
  }

  return (
    <div className="stack result-tables">
      {scalars.length > 0 ? (
        <ScalarTable
          caption={t("result_scalars_h")}
          guide={guides._scalars}
          entries={scalars}
        />
      ) : null}
      {tables.map((tb) => (
        <DataTable
          key={tb.key}
          rows={tb.rows}
          caption={`${tb.key} (${tb.rows.length})`}
          guide={guides[tb.key]}
        />
      ))}
      {nested.map(([k, v]) => (
        <div key={k} className="nested-card">
          <h5 className="table-caption">{k}</h5>
          <ResultView data={v} tableGuides={guides} />
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const { t, pick, lang } = useLocale();
  const [def, setDef] = useState<PipelineDefinition | null>(null);
  const [stepId, setStepId] = useState(0);
  const [taskId, setTaskId] = useState<string>(STEP_OVERVIEW);
  const [query, setQuery] = useState(SAMPLE_QUERIES[0]);
  const [topK, setTopK] = useState(DEFAULT_TOP_K);
  const [enableTemporal, setEnableTemporal] = useState(true);
  const [enableGraph, setEnableGraph] = useState(true);
  const [enableTrust, setEnableTrust] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TaskResult | null>(null);
  const [healthStats, setHealthStats] = useState<{
    steps: number;
    nodes: number;
    chunks: number;
  } | null>(null);
  const [healthOffline, setHealthOffline] = useState(false);
  const [cache, setCache] = useState<Record<string, TaskResult>>({});
  const [academic, setAcademic] = useState<AcademicPackage | null>(null);
  const [academicLoading, setAcademicLoading] = useState(false);

  const health = useMemo(() => {
    if (healthOffline) return t("health_offline");
    if (!healthStats) return "…";
    return t("health_line", healthStats);
  }, [healthOffline, healthStats, t]);

  const step: PipelineStep | undefined = useMemo(
    () => def?.steps.find((s) => s.id === stepId),
    [def, stepId],
  );

  const isStepOverview = taskId === STEP_OVERVIEW;
  const activeTask = useMemo(() => {
    if (!step || isStepOverview) return null;
    return step.tasks.find((t) => t.id === taskId) ?? null;
  }, [step, taskId, isStepOverview]);

  useEffect(() => {
    api
      .health()
      .then((h) => {
        setHealthOffline(false);
        setHealthStats({
          steps: h.pipeline_steps,
          nodes: h.kg_nodes,
          chunks: h.evidence_chunks,
        });
      })
      .catch(() => setHealthOffline(true));
    api
      .pipeline()
      .then((p) => {
        setDef(p);
        setTaskId(STEP_OVERVIEW);
      })
      .catch((e) => setError(String(e)));
  }, []);

  // Entering a parent step always opens its overview first (scientific sequence).
  useEffect(() => {
    if (stepId === 0) return;
    setTaskId(STEP_OVERVIEW);
  }, [stepId]);

  useEffect(() => {
    if (stepId === 0 || isStepOverview) {
      setResult(null);
      return;
    }
    const key = `${stepId}:${taskId}`;
    if (cache[key]) setResult(cache[key]);
    else setResult(null);
  }, [stepId, taskId, cache, isStepOverview]);

  // Auto-load Step-1 catalog (≥300 APA) and coverage matrix when opening those tabs.
  useEffect(() => {
    if (stepId !== 1 || isStepOverview) return;
    if (taskId !== "catalog" && taskId !== "matrix") return;
    const key = `1:${taskId}`;
    if (cache[key]) return;
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.runTask(1, taskId, {});
        if (cancelled) return;
        setResult(res);
        setCache((c) => ({ ...c, [key]: res }));
        if (res.academic) setAcademic(res.academic);
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : String(e));
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [stepId, taskId, isStepOverview, cache]);

  useEffect(() => {
    let cancelled = false;
    async function loadAcademic() {
      // Step 16 is the live product app — skip academic process packs.
      if (stepId === 0 || stepId === 16) {
        setAcademic(null);
        setAcademicLoading(false);
        return;
      }
      setAcademicLoading(true);
      try {
        const pack = isStepOverview
          ? await api.stepAcademic(stepId)
          : await api.taskAcademic(stepId, taskId);
        if (!cancelled) setAcademic(pack);
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : String(e));
          setAcademic(null);
        }
      } finally {
        if (!cancelled) setAcademicLoading(false);
      }
    }
    if (def) void loadAcademic();
    return () => {
      cancelled = true;
    };
  }, [def, stepId, taskId, isStepOverview]);

  const runBody = () => ({
    query,
    top_k: topK,
    enable_temporal: enableTemporal,
    enable_graph: enableGraph,
    enable_trust_score: enableTrust,
  });

  async function runCurrent() {
    if (!taskId || isStepOverview) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.runTask(stepId, taskId, runBody());
      setResult(res);
      setCache((c) => ({ ...c, [`${stepId}:${taskId}`]: res }));
      if (res.academic) setAcademic(res.academic);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }

  async function runAllTasksInStep() {
    if (!step) return;
    setLoading(true);
    setError(null);
    try {
      let last: TaskResult | null = null;
      const nextCache = { ...cache };
      const body = runBody();
      for (const t of step.tasks) {
        const res = await api.runTask(stepId, t.id, body);
        nextCache[`${stepId}:${t.id}`] = res;
        last = res;
      }
      setCache(nextCache);
      if (last) {
        setTaskId(step.tasks[step.tasks.length - 1].id);
        setResult(last);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }

  /** Mark Step-16 console task done when the live app analyzes successfully. */
  function markStep16Progress(payload?: Record<string, unknown>) {
    const synthetic: TaskResult = {
      step_id: 16,
      step_title: "Ứng dụng thực tế",
      step_title_en: "Practical application",
      task_id: "console",
      task_title: "IDS/CTI console",
      task_title_en: "IDS/CTI console",
      action: "app_console",
      elapsed_ms: Number(payload?.latency_ms ?? 0),
      real_computation: true,
      computation_kind: "live_edgr_app",
      result: payload ?? { ok: true },
    };
    setCache((c) => ({ ...c, "16:console": synthetic }));
  }

  const progressDone = useMemo(() => {
    if (!def) return 0;
    let n = 0;
    for (const s of def.steps) {
      for (const t of s.tasks) {
        if (cache[`${s.id}:${t.id}`]) n += 1;
      }
    }
    return n;
  }, [def, cache]);

  const progressTotal = useMemo(() => {
    if (!def) return 0;
    return def.steps.reduce((a, s) => a + s.tasks.length, 0);
  }, [def]);

  return (
    <>
      <header className="hero-banner" aria-label="EDGR banner">
        <img
          src="/edgr-topic-banner.png"
          alt="EDGR — dynamic knowledge graph for CTI and intrusion detection"
          className="edgr-banner-bg"
        />
        <div className="banner-body">
          <div className="banner-copy">
            <p className="banner-kicker">{t("banner_kicker")}</p>
            <h1 className="banner-title">EDGR</h1>
            <p className="banner-desc">
              {pick(
                def?.topic_vi ??
                  "Thuật toán truy hồi đồ thị động dựa trên bằng chứng để giảm ảo giác trong LLM cho phát hiện xâm nhập và tình báo mối đe dọa mạng",
                def?.topic ??
                  "An Evidence-Driven Dynamic Graph Retrieval Algorithm for Hallucination Mitigation in Large Language Models for Intrusion Detection and Cyber Threat Intelligence",
              )}
            </p>
            <p className="banner-meta">
              {t("banner_meta")} · {health}
            </p>
          </div>
          <div className="banner-aside">
            <LanguageMenu />
            <div
              className="progress-pill live-progress"
              title={t("banner_progress_title")}
            >
              {t("banner_progress", {
                done: progressDone,
                total: progressTotal,
              })}
            </div>
          </div>
        </div>
      </header>

      <div className="app-shell">
      {/* Tab 0 + pipeline A→Z — single-row scroll with arrows */}
      <StepRail
        stepId={stepId}
        setStepId={setStepId}
        def={def}
        cache={cache}
        pick={pick}
        t={t}
      />

      {error && <div className="error">{error}</div>}

      {stepId === 0 && (
        <OverviewTab
          topic={def?.topic}
          topicVi={def?.topic_vi}
          onGoStep={(id) => setStepId(id)}
        />
      )}

      {stepId === 16 && step && (
        <section
          className="panel workspace ids-app-workspace"
          style={{ "--step-color": STEP_COLORS[16] } as CSSProperties}
          key={`ids-app-${lang}`}
        >
          <nav className="breadcrumb" aria-label={t("crumb_aria")}>
            <button type="button" onClick={() => setStepId(0)}>
              {t("crumb_overview")}
            </button>
            <span aria-hidden>›</span>
            <strong>
              {t("crumb_step", {
                id: 16,
                title: pick(step.title, step.title_en),
              })}
            </strong>
            <span aria-hidden>›</span>
            <em>{t("ids_app_name")}</em>
          </nav>
          <IdsCtiApp
            color={STEP_COLORS[16]}
            topK={topK}
            onTopKChange={setTopK}
            onAnalyzeSuccess={markStep16Progress}
          />
        </section>
      )}

      {stepId !== 0 && stepId !== 16 && step && (
        <section
          className="panel workspace"
          style={{ "--step-color": STEP_COLORS[step.id] } as CSSProperties}
          key={lang}
        >
          <nav className="breadcrumb" aria-label={t("crumb_aria")}>
            <button type="button" onClick={() => setStepId(0)}>
              {t("crumb_overview")}
            </button>
            <span aria-hidden>›</span>
            <strong>
              {t("crumb_step", {
                id: step.id,
                title: pick(step.title, step.title_en),
              })}
            </strong>
            <span aria-hidden>›</span>
            <em>
              {isStepOverview
                ? t("crumb_step_overview")
                : t("crumb_task", {
                    title: pick(
                      activeTask?.title ?? taskId,
                      activeTask?.title_en ?? taskId,
                    ),
                  })}
            </em>
          </nav>

          <div className="section-head">
            <h2 className="step-title-row">
              <span
                className="step-title-icon"
                style={{
                  background: `${STEP_COLORS[step.id]}18`,
                  borderColor: `${STEP_COLORS[step.id]}55`,
                }}
              >
                <StepIcon stepId={step.id} size={28} />
              </span>
              <span>
                {t("step_heading", {
                  id: step.id,
                  title: pick(step.title, step.title_en),
                })}
              </span>
            </h2>
            <p>{pick(step.goal, step.goal_en ?? step.goal)}</p>
          </div>

          <div className="level-hint">{t("scientific_seq")}</div>

          <div className="task-rail" aria-label={t("task_rail_aria")}>
            <button
              className={`task-chip overview-task ${isStepOverview ? "active" : ""}`}
              onClick={() => setTaskId(STEP_OVERVIEW)}
              style={{ "--step-color": STEP_COLORS[step.id] } as CSSProperties}
              title={t("step_overview")}
            >
              <span className="task-icon overview-dot">Σ</span>
              <span className="task-chip-label">{t("step_overview")}</span>
            </button>
            {step.tasks.map((tTask, idx) => {
              const taskLabel = `${idx + 1}. ${pick(tTask.title, tTask.title_en)}`;
              return (
                <button
                  key={tTask.id}
                  className={`task-chip ${taskId === tTask.id ? "active" : ""} ${cache[`${step.id}:${tTask.id}`] ? "done" : ""}`}
                  onClick={() => setTaskId(tTask.id)}
                  style={{ "--step-color": STEP_COLORS[step.id] } as CSSProperties}
                  title={taskLabel}
                >
                  <TaskIcon stepId={step.id} index={idx} size={20} />
                  <span className="task-chip-label">{taskLabel}</span>
                </button>
              );
            })}
          </div>

          {isStepOverview ? (
            <AcademicPanel
              pack={academic}
              color={STEP_COLORS[step.id]}
              loading={academicLoading}
            />
          ) : (
            <>
              {step.id === 1 && taskId === "catalog" ? (
                <div className="surface child-intro">
                  <p className="catalog-locate muted">
                    {pick(
                      "Danh sách APA (≥300) nằm ở khối «Kết quả» bên dưới — gồm ~15 mục core (citable) + ~320 scaffold. Tab sẽ tự tải khi mở.",
                      "The APA list (≥300) is in the «Results» block below — ~15 citable core + ~320 scaffold entries. This tab auto-loads on open.",
                    )}
                  </p>
                </div>
              ) : null}

              <AcademicPanel
                pack={academic}
                color={STEP_COLORS[step.id]}
                loading={academicLoading}
                hideBlocks={
                  result
                    ? ["nhan_dinh_danh_gia"]
                    : undefined
                }
              />

              <div className="controls-bar">
                <div className="query-inline">
                  <label>{t("query_label")}</label>
                  <select
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  >
                    {SAMPLE_QUERIES.map((q) => (
                      <option key={q} value={q}>
                        {q}
                      </option>
                    ))}
                  </select>
                  <input
                    className="query-edit"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                  <label className="topk-label" title={t("topk_hint")}>
                    {t("topk_label")}
                    <select
                      value={topK}
                      onChange={(e) => setTopK(Number(e.target.value))}
                    >
                      {TOP_K_CHOICES.map((k) => (
                        <option key={k} value={k}>
                          {k === DEFAULT_TOP_K
                            ? t("topk_option_rec", { k })
                            : String(k)}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                <p className="topk-hint muted tiny">{t("topk_hint")}</p>
                {(step.id === 4 ||
                  step.id === 8 ||
                  step.id === 9 ||
                  step.id === 11 ||
                  step.id === 6) && (
                  <fieldset className="ablation-toggles">
                    <legend className="muted tiny">{t("ablation_toggles_h")}</legend>
                    <label className="toggle-chip">
                      <input
                        type="checkbox"
                        checked={enableTemporal}
                        onChange={(e) => setEnableTemporal(e.target.checked)}
                      />
                      {t("toggle_temporal")}
                    </label>
                    <label className="toggle-chip">
                      <input
                        type="checkbox"
                        checked={enableGraph}
                        onChange={(e) => setEnableGraph(e.target.checked)}
                      />
                      {t("toggle_graph")}
                    </label>
                    <label className="toggle-chip">
                      <input
                        type="checkbox"
                        checked={enableTrust}
                        onChange={(e) => setEnableTrust(e.target.checked)}
                      />
                      {t("toggle_trust")}
                    </label>
                  </fieldset>
                )}
                <div className="btn-row">
                  <button
                    className="btn btn-solid"
                    disabled={loading}
                    onClick={runCurrent}
                  >
                    {loading ? t("running") : t("run_this")}
                  </button>
                  <button
                    className="btn btn-outline"
                    disabled={loading}
                    onClick={runAllTasksInStep}
                  >
                    {t("run_step_all", { id: step.id })}
                  </button>
                </div>
                <p className="run-hint muted">{t("run_this_hint")}</p>
              </div>

              <div className="surface result-doc-section" id="sci-runtime">
                <h3>
                  {t("result_h")}
                  {result?.computation_kind ? (
                    <span
                      className={`live-tag kind-${result.real_computation ? "live" : "artifact"}`}
                      title={result.computation_kind}
                    >
                      {result.real_computation
                        ? result.computation_kind
                        : `artifact · ${result.computation_kind}`}
                    </span>
                  ) : null}
                </h3>
                {result ? (
                  <>
                    <div className="meta-line">
                      <span>
                        {pick(
                          result.task_title,
                          result.task_title_en ?? result.task_title,
                        )}
                      </span>
                      <span className="mono">{result.elapsed_ms} ms</span>
                    </div>
                    <ResultReviewPanel
                      review={result.result_review}
                      onJumpHumanEval={() => {
                        setStepId(10);
                        setTaskId("human_eval");
                      }}
                    />
                    <h4 className="result-raw-h">{t("result_raw_h")}</h4>
                    <ResultView
                      data={result.result}
                      tableGuides={
                        result.result_review?.tables ??
                        result.result_review?.evidence?.tables ??
                        null
                      }
                    />
                  </>
                ) : (
                  <p className="muted">{t("result_empty")}</p>
                )}
              </div>
            </>
          )}
        </section>
      )}

      <footer className="app-footer" role="contentinfo">
        <div className="app-footer-inner">
          <p className="footer-copy">
            {t("footer_copy", { year: new Date().getFullYear() })}
          </p>
        </div>
      </footer>
      </div>
    </>
  );
}
