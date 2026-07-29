import { useCallback, useEffect, useState, type CSSProperties, type FormEvent } from "react";
import {
  api,
  type AppAlert,
  type AppAnalyzeResult,
  type AppStatus,
} from "./api";
import { hasResultViz, ResultDataViz } from "./DataViz";
import { useLocale } from "./i18n/LocaleContext";

const QUICK_QUERIES = [
  {
    id: "cve",
    q: "What is CVE-2021-44228 and how is it exploited?",
    label_vi: "CVE-2021-44228",
    label_en: "CVE-2021-44228",
  },
  {
    id: "apt",
    q: "Which ATT&CK techniques does APT29 commonly use?",
    label_vi: "TTP APT29",
    label_en: "APT29 TTPs",
  },
  {
    id: "lateral",
    q: "How can NIDS detect lateral movement?",
    label_vi: "Lateral movement",
    label_en: "Lateral movement",
  },
  {
    id: "clop",
    q: "Which CVE did Cl0p exploit in MOVEit campaigns?",
    label_vi: "Cl0p / MOVEit",
    label_en: "Cl0p / MOVEit",
  },
] as const;

type Props = {
  color: string;
  topK: number;
  onTopKChange?: (k: number) => void;
  onAnalyzeSuccess?: (result: Record<string, unknown>) => void;
};

type InputMode = "query" | "alert";

const TOP_K_CHOICES = [3, 5, 8] as const;

export function IdsCtiApp({
  color,
  topK,
  onTopKChange,
  onAnalyzeSuccess,
}: Props) {
  const { t, pick } = useLocale();
  const [mode, setMode] = useState<InputMode>("alert");
  const [query, setQuery] = useState(QUICK_QUERIES[0].q);
  const [alertJson, setAlertJson] = useState("");
  const [alerts, setAlerts] = useState<AppAlert[]>([]);
  const [queueSize, setQueueSize] = useState(0);
  const [selectedAlertId, setSelectedAlertId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<AppStatus | null>(null);
  const [result, setResult] = useState<AppAnalyzeResult | null>(null);

  const refreshAlerts = useCallback(async () => {
    try {
      const res = await api.appListAlerts(40);
      setAlerts(res.alerts ?? []);
      setQueueSize(res.queue_size ?? 0);
      if (!selectedAlertId && res.alerts?.[0]?.id) {
        setSelectedAlertId(res.alerts[0].id);
      }
    } catch {
      /* ignore while backend warming */
    }
  }, [selectedAlertId]);

  useEffect(() => {
    void api
      .appStatus()
      .then(setStatus)
      .catch(() => setStatus(null));
    void refreshAlerts();
    void api
      .appAlertSample()
      .then((s) => {
        if (!alertJson) {
          setAlertJson(JSON.stringify(s.alert, null, 2));
        }
      })
      .catch(() => undefined);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Light poll for realtime queue while on alert mode
  useEffect(() => {
    if (mode !== "alert") return;
    const id = window.setInterval(() => {
      void refreshAlerts();
    }, 4000);
    return () => window.clearInterval(id);
  }, [mode, refreshAlerts]);

  const runQuery = async (q: string) => {
    const text = q.trim();
    if (!text) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.appAnalyze({
        query: text,
        top_k: topK,
        live_enrich: true,
      });
      setResult(res);
      onAnalyzeSuccess?.(res as Record<string, unknown>);
      void api.appStatus().then(setStatus).catch(() => undefined);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  };

  const ingestAlert = async (analyzeAfter: boolean) => {
    setLoading(true);
    setError(null);
    try {
      let payload: unknown;
      try {
        payload = JSON.parse(alertJson);
      } catch {
        throw new Error(t("ids_app_alert_bad_json"));
      }
      const ing = await api.appIngestAlerts(payload);
      setQueueSize(ing.queue_size ?? 0);
      await refreshAlerts();
      const firstId = ing.alerts?.[0]?.id;
      if (firstId) setSelectedAlertId(firstId);
      if (analyzeAfter && firstId) {
        const res = await api.appAnalyzeAlert(firstId, topK);
        setResult(res);
        onAnalyzeSuccess?.(res as Record<string, unknown>);
      }
      void api.appStatus().then(setStatus).catch(() => undefined);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  };

  const analyzeSelected = async () => {
    if (!selectedAlertId) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.appAnalyzeAlert(selectedAlertId, topK);
      setResult(res);
      onAnalyzeSuccess?.(res as Record<string, unknown>);
      await refreshAlerts();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  };

  const loadSample = async () => {
    try {
      const s = await api.appAlertSample();
      setAlertJson(JSON.stringify(s.alert, null, 2));
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  };

  const onSubmitQuery = (e: FormEvent) => {
    e.preventDefault();
    void runQuery(query);
  };

  const answer = typeof result?.answer === "string" ? result.answer : "";
  const evidence = Array.isArray(result?.evidence) ? result.evidence : [];
  const entities = Array.isArray(result?.entities)
    ? result.entities.map(String)
    : [];
  const stages = Array.isArray(result?.stage_summary) ? result.stage_summary : [];
  const enrich = result?.live_enrichment;
  const vizSource = result && hasResultViz(result) ? result : null;
  const isLive = result?.simulated === false || result?.mode === "live_edgr";
  const abstained = Boolean(result?.abstained);
  const abstainReason = result
    ? pick(
        String(result.abstain_reason_vi ?? ""),
        String(result.abstain_reason_en ?? result.abstain_reason_vi ?? ""),
      )
    : "";

  const showResultBody = Boolean(result && !loading);

  return (
    <div className="ids-app" style={{ "--step-color": color } as CSSProperties}>
      <header className="ids-app-hero">
        <div className="ids-hero-main">
          <p className="ids-app-kicker">{t("ids_app_kicker")}</p>
          <h2 className="ids-app-name">{t("ids_app_name")}</h2>
          <p className="ids-app-tagline">{t("ids_app_tagline")}</p>
        </div>
        <aside className="ids-hero-meta">
          <div className="ids-live-bar">
            <span className="ids-live-pill">{t("ids_app_live_badge")}</span>
            {status ? (
              <span className="ids-live-stats">
                KG {status.kg_nodes}/{status.kg_edges} · evidence{" "}
                {status.evidence_chunks} · alerts{" "}
                {status.alert_queue_size ?? queueSize}
              </span>
            ) : (
              <span className="ids-live-stats">{t("ids_app_live_loading")}</span>
            )}
          </div>
          <p className="ids-live-note">
            {status
              ? pick(status.note_vi ?? "", status.note_en ?? status.note_vi ?? "")
              : t("ids_app_live_promise")}
          </p>
          <label className="ids-topk-label" title={t("topk_hint")}>
            {t("topk_label")}
            <select
              value={topK}
              onChange={(e) => onTopKChange?.(Number(e.target.value))}
            >
              {TOP_K_CHOICES.map((k) => (
                <option key={k} value={k}>
                  {k === 5 ? t("topk_option_rec", { k }) : String(k)}
                </option>
              ))}
            </select>
          </label>
        </aside>
      </header>

      {error ? <div className="error">{error}</div> : null}

      <div className="ids-console">
        <div className="ids-console-input">
          <div className="ids-mode-row" role="tablist" aria-label={t("ids_app_kicker")}>
            <button
              type="button"
              role="tab"
              aria-selected={mode === "alert"}
              className={`ids-mode ${mode === "alert" ? "active" : ""}`}
              onClick={() => setMode("alert")}
            >
              {t("ids_app_mode_alert")}
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={mode === "query"}
              className={`ids-mode ${mode === "query" ? "active" : ""}`}
              onClick={() => setMode("query")}
            >
              {t("ids_app_mode_query")}
            </button>
          </div>

          {mode === "alert" ? (
            <section className="ids-app-panel surface">
              <h3>{t("ids_app_alert_h")}</h3>
              <p className="muted tiny">{t("ids_app_alert_hint")}</p>
              <p className="muted tiny mono">
                POST /api/app/alerts · queue={queueSize}
              </p>
              <div className="ids-ask-actions" style={{ marginBottom: 8 }}>
                <button
                  type="button"
                  className="btn btn-outline"
                  onClick={() => void loadSample()}
                >
                  {t("ids_app_alert_sample")}
                </button>
                <button
                  type="button"
                  className="btn btn-outline"
                  onClick={() => void refreshAlerts()}
                >
                  {t("ids_app_alert_refresh")}
                </button>
              </div>
              <label className="ids-ask-label" htmlFor="ids-alert-json">
                {t("ids_app_alert_json")}
              </label>
              <textarea
                id="ids-alert-json"
                className="ids-ask-input mono"
                rows={10}
                value={alertJson}
                onChange={(e) => setAlertJson(e.target.value)}
                placeholder='{"event_type":"alert","alert":{"signature":"..."}}'
                spellCheck={false}
              />
              <div className="ids-ask-actions">
                <button
                  type="button"
                  className="btn btn-outline"
                  disabled={loading || !alertJson.trim()}
                  onClick={() => void ingestAlert(false)}
                >
                  {t("ids_app_alert_ingest")}
                </button>
                <button
                  type="button"
                  className="btn btn-solid"
                  disabled={loading || !alertJson.trim()}
                  onClick={() => void ingestAlert(true)}
                >
                  {loading
                    ? t("ids_app_analyzing")
                    : t("ids_app_alert_ingest_analyze")}
                </button>
              </div>

              {alerts.length > 0 ? (
                <div className="ids-alert-queue">
                  <h4>
                    {t("ids_app_alert_queue")} ({alerts.length})
                  </h4>
                  <ul>
                    {alerts.map((a) => (
                      <li key={a.id}>
                        <label className="ids-alert-item">
                          <input
                            type="radio"
                            name="alert"
                            checked={selectedAlertId === a.id}
                            onChange={() => setSelectedAlertId(a.id)}
                          />
                          <span>
                            <strong>{a.signature || a.id}</strong>
                            <span className="muted tiny">
                              {" "}
                              {a.src_ip || "?"} → {a.dest_ip || "?"} · sev=
                              {a.severity ?? "?"}
                              {a.analyzed ? ` · ${t("ids_app_alert_done")}` : ""}
                            </span>
                          </span>
                        </label>
                      </li>
                    ))}
                  </ul>
                  <button
                    type="button"
                    className="btn btn-solid"
                    disabled={loading || !selectedAlertId}
                    onClick={() => void analyzeSelected()}
                  >
                    {loading
                      ? t("ids_app_analyzing")
                      : t("ids_app_alert_analyze")}
                  </button>
                </div>
              ) : (
                <p className="muted tiny" style={{ marginTop: 10 }}>
                  {t("ids_app_alert_empty")}
                </p>
              )}
            </section>
          ) : (
            <section className="ids-app-panel surface">
              <h3>{t("ids_app_input_h")}</h3>
              <p className="muted tiny">{t("ids_app_input_hint")}</p>
              <div className="ids-scenario-row">
                {QUICK_QUERIES.map((s) => (
                  <button
                    key={s.id}
                    type="button"
                    className={`ids-scenario ${query === s.q ? "active" : ""}`}
                    onClick={() => setQuery(s.q)}
                  >
                    {pick(s.label_vi, s.label_en)}
                  </button>
                ))}
              </div>
              <form className="ids-ask-form" onSubmit={onSubmitQuery}>
                <label className="ids-ask-label" htmlFor="ids-query">
                  {t("ids_app_query_label")}
                </label>
                <textarea
                  id="ids-query"
                  className="ids-ask-input"
                  rows={4}
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder={t("ids_app_placeholder")}
                />
                <div className="ids-ask-actions">
                  <button
                    type="submit"
                    className="btn btn-solid"
                    disabled={loading || !query.trim()}
                  >
                    {loading ? t("ids_app_analyzing") : t("ids_app_analyze")}
                  </button>
                  <span className="muted tiny">top_k = {topK}</span>
                </div>
              </form>
            </section>
          )}
        </div>

        <section
          className={`ids-app-panel surface ids-console-result${showResultBody ? " has-result" : ""}`}
          id="ids-app-result"
        >
          <h3>
            {t("ids_app_result_h")}
            {isLive ? (
              <span className="ids-live-pill compact">
                {t("ids_app_live_badge")}
              </span>
            ) : null}
          </h3>

          {loading ? (
            <div className="ids-result-empty">
              <p className="muted">{t("ids_app_analyzing")}</p>
            </div>
          ) : null}

          {!result && !loading ? (
            <div className="ids-result-empty">
              <p className="muted">{t("ids_app_empty")}</p>
            </div>
          ) : null}

          {showResultBody && result ? (
            <div className="ids-result-body">
              <div className="ids-result-primary">
                {result.provenance_vi || result.provenance_en ? (
                  <p className="ids-provenance muted tiny">
                    {pick(
                      String(result.provenance_vi ?? ""),
                      String(
                        result.provenance_en ?? result.provenance_vi ?? "",
                      ),
                    )}
                  </p>
                ) : null}

                {abstained ? (
                  <div className="ids-abstain" role="status">
                    <strong>{t("ids_app_abstain")}</strong>
                    <p>{abstainReason || answer}</p>
                  </div>
                ) : answer ? (
                  <div className="ids-answer">
                    <h4>{t("ids_app_answer")}</h4>
                    <p>{answer}</p>
                  </div>
                ) : (
                  <p className="muted">{t("ids_app_no_answer")}</p>
                )}

                <div className="ids-metrics">
                  <div className="ids-metric">
                    <span>{t("ids_app_apply")}</span>
                    <strong>
                      {abstained || result.apply === 0 ? "0" : "1"}
                    </strong>
                  </div>
                  {result.faithfulness != null ? (
                    <div className="ids-metric">
                      <span>{t("ids_app_faith")}</span>
                      <strong>
                        {abstained
                          ? "—"
                          : `${(Number(result.faithfulness) * 100).toFixed(1)}%`}
                      </strong>
                    </div>
                  ) : null}
                  {result.hallucination_rate != null ? (
                    <div className="ids-metric">
                      <span>{t("ids_app_hall")}</span>
                      <strong>
                        {abstained
                          ? "—"
                          : `${(Number(result.hallucination_rate) * 100).toFixed(1)}%`}
                      </strong>
                    </div>
                  ) : null}
                  {result.confidence != null ? (
                    <div className="ids-metric">
                      <span>{t("ids_app_conf")}</span>
                      <strong>
                        {abstained
                          ? "0%"
                          : `${(Number(result.confidence) * 100).toFixed(1)}%`}
                      </strong>
                    </div>
                  ) : null}
                  {result.latency_ms != null ? (
                    <div className="ids-metric">
                      <span>{t("ids_app_latency")}</span>
                      <strong>{Number(result.latency_ms).toFixed(0)} ms</strong>
                    </div>
                  ) : null}
                </div>

                {enrich?.attempted ? (
                  <p className="muted tiny">
                    {t("ids_app_nvd")}:{" "}
                    {enrich.injected?.length
                      ? enrich.injected.join(", ")
                      : t("ids_app_nvd_miss")}
                  </p>
                ) : null}
              </div>

              {(stages.length > 0 ||
                entities.length > 0 ||
                evidence.length > 0 ||
                vizSource) && (
                <div className="ids-result-secondary">
                  {stages.length > 0 ? (
                    <div className="ids-stages">
                      <h4>{t("ids_app_stages")}</h4>
                      <ol>
                        {stages.map((s, i) => (
                          <li key={i}>
                            <strong>
                              φ{String(s.stage ?? i + 1)} ·{" "}
                              {pick(
                                String(s.name_vi ?? ""),
                                String(s.name ?? ""),
                              )}
                            </strong>
                            {s.duration_ms != null ? (
                              <span className="muted">
                                {" "}
                                ({Number(s.duration_ms).toFixed(1)} ms)
                              </span>
                            ) : null}
                          </li>
                        ))}
                      </ol>
                    </div>
                  ) : null}

                  {entities.length > 0 ? (
                    <div className="ids-entities">
                      <h4>{t("ids_app_entities")}</h4>
                      <div className="ids-entity-chips">
                        {entities.map((e) => (
                          <span key={e} className="ids-entity">
                            {e}
                          </span>
                        ))}
                      </div>
                    </div>
                  ) : null}

                  {evidence.length > 0 ? (
                    <div className="ids-evidence">
                      <h4>
                        {t("ids_app_evidence")} ({evidence.length})
                      </h4>
                      <ul>
                        {evidence.map((ev, i) => (
                          <li key={String(ev.id ?? i)}>
                            <strong>{String(ev.id ?? `#${i + 1}`)}</strong>
                            {ev.source != null ? (
                              <span className="muted">
                                {" "}
                                · {String(ev.source)}
                              </span>
                            ) : null}
                            {ev.content != null || ev.text != null ? (
                              <p>{String(ev.content ?? ev.text)}</p>
                            ) : null}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}

                  {vizSource ? (
                    <div className="ids-graph">
                      <h4>{t("ids_app_graph")}</h4>
                      <ResultDataViz data={vizSource} />
                    </div>
                  ) : null}
                </div>
              )}
            </div>
          ) : null}
        </section>
      </div>

      <footer className="ids-app-foot muted tiny">{t("ids_app_foot")}</footer>
    </div>
  );
}
