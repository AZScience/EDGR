import {
  useCallback,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent as ReactPointerEvent,
  type ReactNode,
} from "react";
import {
  ArchitectureDiagram,
  hasResultViz,
  parseArchitectureFromData,
  ResultDataViz,
} from "./DataViz";
import { useLocale } from "./i18n/LocaleContext";
import {
  Formula,
  MathText,
  looksLikeFormula,
  toLatex,
} from "./mathFormat";

export { Formula, MathText, looksLikeFormula, toLatex };

function asRecord(data: unknown): Record<string, unknown> {
  return data && typeof data === "object" && !Array.isArray(data)
    ? (data as Record<string, unknown>)
    : {};
}

function asStringList(v: unknown): string[] {
  if (Array.isArray(v)) return v.map(String);
  if (typeof v === "string") return [v];
  return [];
}

type MathVar = {
  symbol?: string;
  vi?: string;
  en?: string;
  domain?: string;
  good?: string;
};

type MathFormula = {
  id?: string;
  label_vi?: string;
  label_en?: string;
  latex?: string;
  explain_vi?: string;
  explain_en?: string;
  variables?: MathVar[];
  optimize_vi?: string;
  optimize_en?: string;
};

function CritiqueLists({
  data,
  showImproveFormulas = false,
}: {
  data: Record<string, unknown>;
  showImproveFormulas?: boolean;
}) {
  const { t, pick } = useLocale();
  const pros = pick(
    (data.pros_vi as string[]) ?? [],
    (data.pros_en as string[]) ?? (data.pros_vi as string[]) ?? [],
  );
  const cons = pick(
    (data.cons_vi as string[]) ?? [],
    (data.cons_en as string[]) ?? (data.cons_vi as string[]) ?? [],
  );
  const improve = pick(
    (data.improve_vi as string[]) ?? [],
    (data.improve_en as string[]) ?? (data.improve_vi as string[]) ?? [],
  );
  const improveMath = pick(
    (data.improve_math_vi as string[]) ?? [],
    (data.improve_math_en as string[]) ?? (data.improve_math_vi as string[]) ?? [],
  );
  const improveAlgo = pick(
    (data.improve_algo_vi as string[]) ?? [],
    (data.improve_algo_en as string[]) ?? (data.improve_algo_vi as string[]) ?? [],
  );
  const prosDetail = pick(
    String(data.pros_detail_vi || ""),
    String(data.pros_detail_en || ""),
  );
  const consDetail = pick(
    String(data.cons_detail_vi || ""),
    String(data.cons_detail_en || ""),
  );
  const improveDetail = pick(
    String(data.improve_detail_vi || ""),
    String(data.improve_detail_en || ""),
  );
  const improveForms = Array.isArray(data.improve_formulas)
    ? (data.improve_formulas as MathFormula[])
    : [];

  if (
    !pros.length &&
    !cons.length &&
    !improve.length &&
    !improveMath.length &&
    !improveAlgo.length &&
    !prosDetail &&
    !consDetail &&
    !improveDetail &&
    !improveForms.length
  ) {
    return null;
  }

  return (
    <div className="critique-grid detailed">
      {(pros.length || prosDetail) && (
        <div className="critique-card good">
          <strong>{t("critique_pros")}</strong>
          {prosDetail ? (
            <MathText text={prosDetail} as="p" className="critique-prose" />
          ) : null}
          {pros.length ? (
            <ul>
              {pros.map((x, i) => (
                <MathText key={i} text={x} as="li" />
              ))}
            </ul>
          ) : null}
        </div>
      )}
      {(cons.length || consDetail) && (
        <div className="critique-card warn">
          <strong>{t("critique_cons")}</strong>
          {consDetail ? (
            <MathText text={consDetail} as="p" className="critique-prose" />
          ) : null}
          {cons.length ? (
            <ul>
              {cons.map((x, i) => (
                <MathText key={i} text={x} as="li" />
              ))}
            </ul>
          ) : null}
        </div>
      )}
      {(improve.length || improveDetail || improveForms.length > 0) && (
        <div className="critique-card improve">
          <strong>{t("critique_improve")}</strong>
          {improveDetail ? (
            <MathText text={improveDetail} as="p" className="critique-prose" />
          ) : null}
          {improve.length ? (
            <ul>
              {improve.map((x, i) => (
                <MathText key={i} text={x} as="li" />
              ))}
            </ul>
          ) : null}
          {showImproveFormulas && improveForms.length > 0 ? (
            <div className="improve-formulas">
              <div className="math-subhead">{t("critique_improve_math")}</div>
              {improveForms.map((f, i) => {
                const label = pick(
                  f.label_vi || t("math_formula"),
                  f.label_en || t("math_formula"),
                );
                const explain = pick(f.explain_vi || "", f.explain_en || "");
                return (
                  <article key={String(f.id ?? i)} className="math-card nested">
                    <div className="math-label">{label}</div>
                    {f.latex ? <Formula expr={f.latex} /> : null}
                    {explain ? (
                      <div className="math-explain">
                        <MathText text={explain} as="p" />
                      </div>
                    ) : null}
                  </article>
                );
              })}
            </div>
          ) : null}
        </div>
      )}
      {improveMath.length ? (
        <div className="critique-card improve">
          <strong>{t("critique_improve_math")}</strong>
          <ul>
            {improveMath.map((x, i) => (
              <MathText key={i} text={x} as="li" />
            ))}
          </ul>
        </div>
      ) : null}
      {improveAlgo.length ? (
        <div className="critique-card improve">
          <strong>{t("critique_improve_algo")}</strong>
          <ul>
            {improveAlgo.map((x, i) => (
              <MathText key={i} text={x} as="li" />
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}

export function MathModelView({ data }: { data: unknown }) {
  const { t, pick, lang } = useLocale();
  const r = asRecord(data);
  const formulas = Array.isArray(r.formulas)
    ? (r.formulas as MathFormula[])
    : null;
  const role = pick(String(r.role_vi || ""), String(r.role_en || ""));
  const narrative = pick(
    String(r.narrative_vi || ""),
    String(r.narrative_en || ""),
  );

  if (formulas && formulas.length) {
    return (
      <div className="model-math rich" key={lang}>
        {role ? (
          <p className="math-role">
            <strong>{t("math_role")}: </strong>
            {role}
          </p>
        ) : null}
        {narrative ? (
          <MathText text={narrative} as="p" className="sci-narrative" />
        ) : null}
        <div
          className={`math-formula-grid${formulas.length > 1 ? " cols-2" : ""}`}
        >
          {formulas.map((f, i) => {
            const label = pick(
              f.label_vi || t("math_formula"),
              f.label_en || t("math_formula"),
            );
            const explain = pick(f.explain_vi || "", f.explain_en || "");
            const optimize = pick(f.optimize_vi || "", f.optimize_en || "");
            return (
              <article key={String(f.id ?? i)} className="math-card">
                <div className="math-label">{label}</div>
                {f.latex ? <Formula expr={f.latex} /> : null}
                {explain ? (
                  <div className="math-explain">
                    <MathText text={explain} as="p" />
                  </div>
                ) : null}
                {f.variables && f.variables.length > 0 ? (
                  <div className="math-vars">
                    <div className="math-subhead">{t("math_vars")}</div>
                    <table>
                      <thead>
                        <tr>
                          <th>{t("math_sym")}</th>
                          <th>{t("math_meaning")}</th>
                          <th>{t("math_domain")}</th>
                          <th>{t("math_good")}</th>
                        </tr>
                      </thead>
                      <tbody>
                        {f.variables.map((v, j) => (
                          <tr key={j}>
                            <td className="sym">
                              {v.symbol ? (
                                <Formula expr={v.symbol} display={false} />
                              ) : (
                                "—"
                              )}
                            </td>
                            <td>
                              <MathText text={pick(v.vi || "—", v.en || "—")} />
                            </td>
                            <td>
                              {v.domain ? (
                                looksLikeFormula(v.domain) ? (
                                  <Formula expr={v.domain} display={false} />
                                ) : (
                                  <MathText text={v.domain} />
                                )
                              ) : (
                                "—"
                              )}
                            </td>
                            <td className="good">
                              {v.good ? <MathText text={v.good} /> : "—"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : null}
                {optimize ? (
                  <div className="math-optimize">
                    <div className="math-subhead">{t("math_optimize")}</div>
                    <MathText text={optimize} as="p" />
                  </div>
                ) : null}
              </article>
            );
          })}
        </div>
        {r.note_vi || r.note_en ? (
          <div className="math-note">
            <p>{pick(String(r.note_vi || ""), String(r.note_en || ""))}</p>
          </div>
        ) : null}
        <CritiqueLists data={r} showImproveFormulas />
      </div>
    );
  }

  const entries = Object.entries(r).filter(
    ([k]) => !["live", "live_system", "lang", "note_vi", "note_en"].includes(k),
  );
  if (!entries.length && typeof data === "string") {
    return looksLikeFormula(data) ? (
      <Formula expr={data} />
    ) : (
      <div className="formula-fallback">{data}</div>
    );
  }
  return (
    <div className="model-math">
      {entries.map(([k, v]) => (
        <div key={k} className="math-row">
          <div className="math-label">{labelize(k)}</div>
          {typeof v === "string" ? (
            looksLikeFormula(v) ? (
              <Formula expr={v} />
            ) : (
              <div className="formula-fallback">{v}</div>
            )
          ) : Array.isArray(v) ? (
            <div className="math-stack">
              {v.map((x, i) =>
                looksLikeFormula(String(x)) ? (
                  <Formula key={i} expr={String(x)} />
                ) : (
                  <div key={i} className="formula-fallback">
                    {String(x)}
                  </div>
                ),
              )}
            </div>
          ) : (
            <div className="formula-fallback">{summarizeObj(v)}</div>
          )}
        </div>
      ))}
    </div>
  );
}

function labelize(k: string) {
  return k
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function useSceneTilt() {
  const ref = useRef<HTMLDivElement>(null);
  const [active, setActive] = useState(false);

  const onMove = useCallback((e: ReactPointerEvent<HTMLDivElement>) => {
    const el = ref.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) return;
    const x = (e.clientX - r.left) / r.width - 0.5;
    const y = (e.clientY - r.top) / r.height - 0.5;
    el.style.setProperty("--tilt-x", `${(-y * 10).toFixed(2)}deg`);
    el.style.setProperty("--tilt-y", `${(x * 14).toFixed(2)}deg`);
    setActive(true);
  }, []);

  const onLeave = useCallback(() => {
    const el = ref.current;
    if (!el) return;
    el.style.setProperty("--tilt-x", "0deg");
    el.style.setProperty("--tilt-y", "0deg");
    setActive(false);
  }, []);

  return { ref, onMove, onLeave, active };
}

function cleanStepLabel(step: string) {
  return step.replace(/^\d+\.\s*/, "").trim();
}

export function AlgorithmModelView({ data }: { data: unknown }) {
  const { t, pick } = useLocale();
  const r = asRecord(data);
  const name = pick(
    String(r.name_vi ?? r.name ?? r.algorithm ?? "Thuật toán"),
    String(r.name_en ?? r.name ?? r.algorithm ?? "Algorithm"),
  );
  const steps = asStringList(r.pseudocode ?? r.steps ?? r.algo ?? []);
  const complexity = r.complexity ? String(r.complexity) : null;
  const mathIds = Array.isArray(r.math_ids)
    ? (r.math_ids as string[])
    : [];
  const narrative = pick(
    String(r.narrative_vi || ""),
    String(r.narrative_en || ""),
  );
  const stepExplain = pick(
    (r.step_explain_vi as string[]) ?? [],
    (r.step_explain_en as string[]) ?? (r.step_explain_vi as string[]) ?? [],
  );
  const improved = asStringList(r.improved_pseudocode ?? []);

  const skipKeys = new Set([
    "name",
    "name_vi",
    "name_en",
    "note",
    "complexity",
    "pseudocode",
    "steps",
    "algo",
    "math_ids",
    "narrative_vi",
    "narrative_en",
    "step_explain_vi",
    "step_explain_en",
    "improved_pseudocode",
    "pros_vi",
    "pros_en",
    "pros_detail_vi",
    "pros_detail_en",
    "cons_vi",
    "cons_en",
    "cons_detail_vi",
    "cons_detail_en",
    "improve_vi",
    "improve_en",
    "improve_detail_vi",
    "improve_detail_en",
    "improve_math_vi",
    "improve_math_en",
    "improve_algo_vi",
    "improve_algo_en",
    "improve_formulas",
  ]);
  const resolved =
    steps.length > 0
      ? steps
      : Object.keys(r)
          .filter((k) => !skipKeys.has(k))
          .map((k) => `${k}: ${String(r[k])}`);

  return (
    <div className="model-algo">
      <div className="algo-title">{name}</div>
      {narrative ? <p className="sci-narrative">{narrative}</p> : null}
      {mathIds.length ? (
        <div className="algo-math-link">
          <strong>{t("algo_math_link")}: </strong>
          <code>{mathIds.join(" · ")}</code>
        </div>
      ) : null}
      {complexity ? (
        <div className="algo-complexity">
          <span>{t("algo_complexity")}</span>
          <Formula expr={complexity} display={false} />
        </div>
      ) : null}
      <AlgoFlow3D
        steps={resolved.length ? resolved : [String(data)]}
        caption={t("algo_caption")}
      />
      {stepExplain.length ? (
        <div className="algo-step-explain">
          <strong>{t("algo_step_explain")}</strong>
          <ul>
            {stepExplain.map((x, i) => (
              <MathText key={i} text={x} as="li" />
            ))}
          </ul>
        </div>
      ) : null}
      <CritiqueLists data={r} />
      {improved.length ? (
        <div className="algo-improved">
          <strong>{t("algo_improved_h")}</strong>
          <ol className="improved-pseudo">
            {improved.map((s, i) => (
              <li key={i}>
                <code>{s}</code>
              </li>
            ))}
          </ol>
        </div>
      ) : null}
    </div>
  );
}

function AlgoFlow3D({ steps, caption }: { steps: string[]; caption: string }) {
  const { t } = useLocale();
  const tilt = useSceneTilt();
  const n = Math.max(steps.length, 1);

  return (
    <div
      className={`viz3d algo-3d ${tilt.active ? "is-tilting" : ""}`}
      ref={tilt.ref}
      onPointerMove={tilt.onMove}
      onPointerLeave={tilt.onLeave}
      role="img"
      aria-label={caption}
    >
      <div className="viz3d-hint">{t("math_tilt")}</div>
      <div className="viz3d-stage">
        <div className="viz3d-board algo-board">
          <div className="viz3d-floor" aria-hidden />
          <div className="algo-cascade" style={{ "--n": n } as CSSProperties}>
            {steps.map((step, i) => (
              <div
                key={i}
                className="iso-block algo-block"
                style={{ "--i": i, "--z": n - i } as CSSProperties}
              >
                <div className="iso-prism">
                  <span className="iso-face top" aria-hidden />
                  <span className="iso-face side" aria-hidden />
                  <div className="iso-face front">
                    <span className="iso-idx">{i + 1}</span>
                    <span className="iso-text">{cleanStepLabel(step)}</span>
                  </div>
                </div>
                {i < steps.length - 1 ? (
                  <div className="iso-pipe vertical" aria-hidden>
                    <span />
                  </div>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      </div>
      <ol className="viz3d-legend">
        {steps.map((step, i) => (
          <li key={i}>
            <b>{i + 1}</b>
            <span>{cleanStepLabel(step)}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}

function isPublicationManuscript(r: Record<string, unknown>): boolean {
  return (
    r.kind === "publication_manuscript" ||
    (Array.isArray(r.sections) &&
      r.sections.length > 0 &&
      (typeof r.working_title === "string" ||
        typeof r.contribution_claim_vi === "string" ||
        typeof r.contribution_claim_en === "string"))
  );
}

function isPublicationPlan(r: Record<string, unknown>): boolean {
  return (
    r.kind === "publication_plan" ||
    ((typeof r.strategy_vi === "string" || typeof r.strategy_en === "string") &&
      Array.isArray(r.timeline_hint))
  );
}

function isPracticalApps(r: Record<string, unknown>): boolean {
  return (
    r.kind === "practical_applications" ||
    (Array.isArray(r.successes) && Array.isArray(r.failures))
  );
}

function isAppProduct(r: Record<string, unknown>): boolean {
  return (
    r.kind === "ids_cti_app_product" ||
    (typeof r.app_name_vi === "string" &&
      Array.isArray(r.capabilities_vi ?? r.capabilities_en) &&
      Array.isArray(r.architecture_flow))
  );
}

/** Step-13 manuscript frame: claim, abstract, sections, integrity. */
export function PublicationManuscriptView({ data }: { data: unknown }) {
  const { t, pick } = useLocale();
  const r = asRecord(data);
  const title = pick(
    String(r.working_title_vi ?? r.working_title ?? ""),
    String(r.working_title ?? r.working_title_vi ?? ""),
  );
  const claim = pick(
    String(r.contribution_claim_vi ?? ""),
    String(r.contribution_claim_en ?? r.contribution_claim_vi ?? ""),
  );
  const abstract = pick(
    String(r.abstract_draft_vi ?? ""),
    String(r.abstract_draft_en ?? r.abstract_draft_vi ?? ""),
  );
  const how = pick(
    String(r.how_to_use_vi ?? r.explain_vi ?? ""),
    String(r.how_to_use_en ?? r.explain_en ?? r.how_to_use_vi ?? ""),
  );
  const novelty = pick(
    (r.novelty_bullets_vi as unknown) ?? [],
    (r.novelty_bullets_en as unknown) ?? r.novelty_bullets_vi ?? [],
  );
  const noveltyList = asStringList(novelty);
  const themes = asStringList(
    pick(
      (r.themes_vi as unknown) ?? [],
      (r.themes_en as unknown) ?? r.themes_vi ?? [],
    ),
  );
  const keywords = asStringList(r.keywords ?? []);
  const maps = Array.isArray(r.maps_to_steps)
    ? (r.maps_to_steps as unknown[]).map(String)
    : [];
  const venues = Array.isArray(r.venue_targets)
    ? (r.venue_targets as Array<Record<string, unknown> | string>)
    : [];
  const sections = Array.isArray(r.sections)
    ? (r.sections as Array<Record<string, unknown>>)
    : [];
  const integrity = asRecord(r.integrity);
  const rules = asStringList(
    pick(
      (integrity.rules_vi as unknown) ?? [],
      (integrity.rules_en as unknown) ?? integrity.rules_vi ?? [],
    ),
  );
  const checks = asStringList(
    pick(
      (integrity.self_check_vi as unknown) ?? [],
      (integrity.self_check_en as unknown) ?? integrity.self_check_vi ?? [],
    ),
  );
  const integrityTitle = pick(
    String(integrity.title_vi ?? ""),
    String(integrity.title_en ?? integrity.title_vi ?? ""),
  );

  return (
    <article className="pub-manuscript">
      {how ? <p className="pub-howto muted">{how}</p> : null}
      {title ? <h3 className="pub-title">{title}</h3> : null}
      {themes.length > 0 ? (
        <p className="pub-keywords muted tiny">
          <strong>{t("pub_themes_h")}: </strong>
          {themes.join(" · ")}
        </p>
      ) : null}
      {(r.manuscript_markdown_vi || r.manuscript_markdown_en) && (
        <div className="pub-download-row">
          <button
            type="button"
            className="btn ghost"
            onClick={() => {
              const md = String(
                pick(
                  r.manuscript_markdown_vi ?? "",
                  r.manuscript_markdown_en ?? r.manuscript_markdown_vi ?? "",
                ),
              );
              const blob = new Blob([md], {
                type: "text/markdown;charset=utf-8",
              });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = "EDGR_scientific_paper.md";
              a.click();
              URL.revokeObjectURL(url);
            }}
          >
            {t("pub_download_md")}
          </button>
        </div>
      )}
      {claim ? (
        <section className="pub-block">
          <h4>{t("pub_claim_h")}</h4>
          <p className="pub-claim">{claim}</p>
        </section>
      ) : null}
      {abstract ? (
        <section className="pub-block">
          <h4>{t("pub_abstract_h")}</h4>
          <p className="pub-prose">{abstract}</p>
        </section>
      ) : null}
      {keywords.length > 0 ? (
        <p className="pub-keywords muted tiny">
          <strong>{t("pub_keywords")}: </strong>
          {keywords.join(" · ")}
        </p>
      ) : null}
      {maps.length > 0 ? (
        <p className="pub-maps muted tiny">
          <strong>{t("pub_maps_steps")}: </strong>
          {maps.join(", ")}
        </p>
      ) : null}
      {noveltyList.length > 0 ? (
        <section className="pub-block">
          <h4>{t("pub_novelty_h")}</h4>
          <ul>
            {noveltyList.map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
        </section>
      ) : null}
      {venues.length > 0 ? (
        <section className="pub-block">
          <h4>{t("pub_venues_h")}</h4>
          <ul className="pub-venues">
            {venues.map((v, i) => {
              if (typeof v === "string") {
                return <li key={i}>{v}</li>;
              }
              const name = String(v.name ?? "");
              const why = pick(
                String(v.why_vi ?? ""),
                String(v.why_en ?? v.why_vi ?? ""),
              );
              return (
                <li key={i}>
                  <strong>{name}</strong>
                  {why ? <span className="muted"> — {why}</span> : null}
                </li>
              );
            })}
          </ul>
        </section>
      ) : null}
      {sections.length > 0 ? (
        <section className="pub-block pub-sections">
          <h4>{t("pub_sections_h")}</h4>
          {sections.map((sec, i) => {
            const name = pick(
              String(sec.name_vi ?? sec.name_en ?? ""),
              String(sec.name_en ?? sec.name_vi ?? ""),
            );
            const goal = pick(
              String(sec.goal_vi ?? ""),
              String(sec.goal_en ?? sec.goal_vi ?? ""),
            );
            const draft = pick(
              String(sec.draft_vi ?? ""),
              String(sec.draft_en ?? sec.draft_vi ?? ""),
            );
            const pitfalls = pick(
              String(sec.pitfalls_vi ?? ""),
              String(sec.pitfalls_en ?? sec.pitfalls_vi ?? ""),
            );
            const cites = asStringList(sec.must_cite ?? []);
            const arts = asStringList(sec.pipeline_artifacts ?? []);
            return (
              <details
                key={i}
                className="pub-section"
                open={
                  String(r.status ?? "") === "manuscript_complete" || i < 2
                }
              >
                <summary>{name || `§${i + 1}`}</summary>
                <div className="pub-section-body">
                  {goal && String(r.status ?? "") !== "manuscript_complete" ? (
                    <p>
                      <strong>{t("pub_sec_goal")}: </strong>
                      {goal}
                    </p>
                  ) : null}
                  {draft ? (
                    <div className="pub-prose pub-prose-body">
                      {draft.split(/\n{2,}/).map((para, pi) => (
                        <p key={pi}>{para}</p>
                      ))}
                    </div>
                  ) : null}
                  {String(r.status ?? "") !== "manuscript_complete" &&
                  cites.length > 0 ? (
                    <p className="muted tiny">
                      <strong>{t("pub_must_cite")}: </strong>
                      {cites.join(", ")}
                    </p>
                  ) : null}
                  {String(r.status ?? "") !== "manuscript_complete" &&
                  arts.length > 0 ? (
                    <p className="muted tiny">
                      <strong>{t("pub_artifacts")}: </strong>
                      {arts.join(" · ")}
                    </p>
                  ) : null}
                  {pitfalls &&
                  String(r.status ?? "") !== "manuscript_complete" ? (
                    <p className="pub-pitfall">
                      <strong>{t("pub_pitfalls")}: </strong>
                      {pitfalls}
                    </p>
                  ) : null}
                </div>
              </details>
            );
          })}
        </section>
      ) : null}
      {rules.length > 0 || checks.length > 0 ? (
        <section className="pub-block pub-integrity">
          <h4>{integrityTitle || t("pub_integrity_h")}</h4>
          {rules.length > 0 ? (
            <ul>
              {rules.map((x, i) => (
                <li key={i}>{x}</li>
              ))}
            </ul>
          ) : null}
          {checks.length > 0 ? (
            <>
              <p>
                <strong>{t("pub_self_check")}</strong>
              </p>
              <ol>
                {checks.map((x, i) => (
                  <li key={i}>{x}</li>
                ))}
              </ol>
            </>
          ) : null}
        </section>
      ) : null}
      {r.live_artifacts && typeof r.live_artifacts === "object" ? (
        <section className="pub-block pub-live">
          <h4>{t("pub_live_h")}</h4>
          <pre className="result-block pub-live-pre">
            {JSON.stringify(r.live_artifacts, null, 2)}
          </pre>
        </section>
      ) : null}
    </article>
  );
}

/** Step-16 product brief: IDS/CTI practical application. */
export function AppProductView({ data }: { data: unknown }) {
  const { t, pick } = useLocale();
  const r = asRecord(data);
  const name = pick(
    String(r.app_name_vi ?? ""),
    String(r.app_name_en ?? r.app_name_vi ?? ""),
  );
  const tagline = pick(
    String(r.tagline_vi ?? ""),
    String(r.tagline_en ?? r.tagline_vi ?? ""),
  );
  const problem = pick(
    String(r.problem_vi ?? ""),
    String(r.problem_en ?? r.problem_vi ?? ""),
  );
  const how = pick(
    String(r.how_to_use_vi ?? r.explain_vi ?? ""),
    String(r.how_to_use_en ?? r.explain_en ?? r.how_to_use_vi ?? ""),
  );
  const users = asStringList(
    pick((r.users_vi as unknown) ?? [], (r.users_en as unknown) ?? r.users_vi ?? []),
  );
  const caps = asStringList(
    pick(
      (r.capabilities_vi as unknown) ?? [],
      (r.capabilities_en as unknown) ?? r.capabilities_vi ?? [],
    ),
  );
  const nonGoals = asStringList(
    pick(
      (r.non_goals_vi as unknown) ?? [],
      (r.non_goals_en as unknown) ?? r.non_goals_vi ?? [],
    ),
  );
  const flow = asStringList(r.architecture_flow ?? r.flow ?? []);
  const deps = Array.isArray(r.depends_on_steps)
    ? (r.depends_on_steps as unknown[]).map(String)
    : [];

  return (
    <article className="pub-manuscript app-product">
      {how ? <p className="pub-howto muted">{how}</p> : null}
      {name ? <h3 className="pub-title">{name}</h3> : null}
      {tagline ? <p className="pub-claim">{tagline}</p> : null}
      {problem ? (
        <section className="pub-block">
          <h4>{t("apps_problem_h")}</h4>
          <p className="pub-prose">{problem}</p>
        </section>
      ) : null}
      {users.length > 0 ? (
        <section className="pub-block">
          <h4>{t("apps_users_h")}</h4>
          <ul>
            {users.map((u, i) => (
              <li key={i}>{u}</li>
            ))}
          </ul>
        </section>
      ) : null}
      {caps.length > 0 ? (
        <section className="pub-block">
          <h4>{t("apps_caps_h")}</h4>
          <ol>
            {caps.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ol>
        </section>
      ) : null}
      {flow.length > 0 ? (
        <section className="pub-block">
          <h4>{t("apps_arch_h")}</h4>
          <ol className="app-arch-flow">
            {flow.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
        </section>
      ) : null}
      {deps.length > 0 ? (
        <p className="muted tiny">
          <strong>{t("pub_maps_steps")}: </strong>
          {deps.join(", ")}
        </p>
      ) : null}
      {nonGoals.length > 0 ? (
        <section className="pub-block">
          <h4>{t("apps_nongoals_h")}</h4>
          <ul>
            {nonGoals.map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
        </section>
      ) : null}
    </article>
  );
}

/** Step-16 practical applications: success vs failure cases. */
export function PracticalAppsView({ data }: { data: unknown }) {
  const { t, pick } = useLocale();
  const r = asRecord(data);
  const title = pick(
    String(r.title_vi ?? ""),
    String(r.title_en ?? r.title_vi ?? ""),
  );
  const lead = pick(
    String(r.lead_vi ?? ""),
    String(r.lead_en ?? r.lead_vi ?? ""),
  );
  const how = pick(
    String(r.how_to_use_vi ?? r.explain_vi ?? ""),
    String(r.how_to_use_en ?? r.explain_en ?? r.how_to_use_vi ?? ""),
  );
  const successes = Array.isArray(r.successes)
    ? (r.successes as Array<Record<string, unknown>>)
    : [];
  const failures = Array.isArray(r.failures)
    ? (r.failures as Array<Record<string, unknown>>)
    : [];
  const takeaways = asStringList(
    pick(
      (r.committee_takeaway_vi as unknown) ?? [],
      (r.committee_takeaway_en as unknown) ?? r.committee_takeaway_vi ?? [],
    ),
  );
  const clf = asRecord(r.query_classification);
  const matched = Array.isArray(clf.matched_cases)
    ? (clf.matched_cases as Array<Record<string, unknown>>)
    : [];

  const renderCase = (
    c: Record<string, unknown>,
    bucket: "success" | "failure",
  ) => {
    const name = pick(
      String(c.title_vi ?? ""),
      String(c.title_en ?? c.title_vi ?? ""),
    );
    const scenario = pick(
      String(c.scenario_vi ?? ""),
      String(c.scenario_en ?? c.scenario_vi ?? ""),
    );
    const why = pick(
      String(c.why_works_vi ?? c.why_fails_vi ?? ""),
      String(
        c.why_works_en ??
          c.why_fails_en ??
          c.why_works_vi ??
          c.why_fails_vi ??
          "",
      ),
    );
    const boundary = pick(
      String(c.boundary_vi ?? c.mitigation_vi ?? ""),
      String(
        c.boundary_en ??
          c.mitigation_en ??
          c.boundary_vi ??
          c.mitigation_vi ??
          "",
      ),
    );
    const honest = pick(
      String(c.honest_line_vi ?? ""),
      String(c.honest_line_en ?? c.honest_line_vi ?? ""),
    );
    const arts = asStringList(c.pipeline_artifacts ?? []);
    const hint = String(c.demo_query_hint ?? "");
    return (
      <details key={String(c.id)} className={`pub-section app-case app-${bucket}`}>
        <summary>
          <span className={`app-badge app-badge-${bucket}`}>
            {String(c.id)}
          </span>{" "}
          {name}
        </summary>
        <div className="pub-section-body">
          {scenario ? (
            <p>
              <strong>{t("apps_scenario")}: </strong>
              {scenario}
            </p>
          ) : null}
          {why ? (
            <p className="pub-prose">
              <strong>
                {bucket === "success" ? t("apps_why_works") : t("apps_why_fails")}
                :{" "}
              </strong>
              {why}
            </p>
          ) : null}
          {boundary ? (
            <p>
              <strong>
                {bucket === "success" ? t("apps_boundary") : t("apps_mitigation")}
                :{" "}
              </strong>
              {boundary}
            </p>
          ) : null}
          {honest ? <p className="pub-pitfall">{honest}</p> : null}
          {arts.length > 0 ? (
            <p className="muted tiny">
              <strong>{t("pub_artifacts")}: </strong>
              {arts.join(" · ")}
            </p>
          ) : null}
          {hint ? (
            <p className="muted tiny">
              <strong>{t("apps_query_hint")}: </strong>
              <code>{hint}</code>
            </p>
          ) : null}
        </div>
      </details>
    );
  };

  return (
    <article className="pub-manuscript app-practical">
      {how ? <p className="pub-howto muted">{how}</p> : null}
      {title ? <h3 className="pub-title">{title}</h3> : null}
      {lead ? <p className="pub-prose">{lead}</p> : null}

      {Object.keys(clf).length > 0 ? (
        <section className="pub-block app-classify">
          <h4>{t("apps_classify_h")}</h4>
          <p>
            <strong>{t("apps_lean")}: </strong>
            {pick(String(clf.lean_vi ?? ""), String(clf.lean_en ?? clf.lean_vi ?? ""))}
          </p>
          {clf.note_vi || clf.note_en ? (
            <p className="muted tiny">
              {pick(String(clf.note_vi ?? ""), String(clf.note_en ?? clf.note_vi ?? ""))}
            </p>
          ) : null}
          {matched.length > 0 ? (
            <ul>
              {matched.map((m, i) => (
                <li key={i}>
                  <span
                    className={`app-badge app-badge-${String(m.bucket) === "failure" ? "failure" : "success"}`}
                  >
                    {String(m.id)}
                  </span>{" "}
                  {pick(
                    String(m.title_vi ?? ""),
                    String(m.title_en ?? m.title_vi ?? ""),
                  )}
                </li>
              ))}
            </ul>
          ) : null}
        </section>
      ) : null}

      <section className="pub-block">
        <h4>
          {t("apps_success_h")}{" "}
          <span className="muted tiny">({successes.length})</span>
        </h4>
        {successes.map((c) => renderCase(c, "success"))}
      </section>

      <section className="pub-block">
        <h4>
          {t("apps_failure_h")}{" "}
          <span className="muted tiny">({failures.length})</span>
        </h4>
        {failures.map((c) => renderCase(c, "failure"))}
      </section>

      {takeaways.length > 0 ? (
        <section className="pub-block">
          <h4>{t("apps_takeaway_h")}</h4>
          <ul>
            {takeaways.map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
        </section>
      ) : null}
    </article>
  );
}

/** Step-13 publication plan (strategy, overlap, timeline). */
export function PublicationPlanView({ data }: { data: unknown }) {
  const { t, pick } = useLocale();
  const r = asRecord(data);
  const strategy = pick(
    String(r.strategy_vi ?? r.strategy ?? ""),
    String(r.strategy_en ?? r.strategy ?? r.strategy_vi ?? ""),
  );
  const overlap = pick(
    String(r.overlap_control_vi ?? ""),
    String(r.overlap_control_en ?? r.overlap_control_vi ?? ""),
  );
  const readiness = asStringList(
    pick(
      (r.committee_readiness_vi as unknown) ?? [],
      (r.committee_readiness_en as unknown) ?? r.committee_readiness_vi ?? [],
    ),
  );
  const timeline = Array.isArray(r.timeline_hint)
    ? (r.timeline_hint as Array<Record<string, unknown>>)
    : [];
  const papers = Array.isArray(r.papers)
    ? (r.papers as Array<Record<string, unknown>>)
    : [];
  const integrity = asRecord(r.integrity);
  const rules = asStringList(
    pick(
      (integrity.rules_vi as unknown) ?? [],
      (integrity.rules_en as unknown) ?? integrity.rules_vi ?? [],
    ),
  );

  return (
    <article className="pub-manuscript pub-plan">
      {strategy ? (
        <section className="pub-block">
          <h4>{t("pub_strategy_h")}</h4>
          <p className="pub-prose">{strategy}</p>
        </section>
      ) : null}
      {overlap ? (
        <section className="pub-block">
          <h4>{t("pub_overlap_h")}</h4>
          <p className="pub-prose">{overlap}</p>
        </section>
      ) : null}
      {timeline.length > 0 ? (
        <section className="pub-block">
          <h4>{t("pub_timeline_h")}</h4>
          <ol>
            {timeline.map((row, i) => (
              <li key={i}>
                <strong>{String(row.phase ?? "")}</strong>
                {" — "}
                {pick(
                  String(row.output_vi ?? row.output ?? ""),
                  String(row.output_en ?? row.output ?? row.output_vi ?? ""),
                )}
              </li>
            ))}
          </ol>
        </section>
      ) : null}
      {papers.length > 0 ? (
        <section className="pub-block">
          <h4>{t("pub_papers_h")}</h4>
          <ul>
            {papers.map((p, i) => {
              const themes = pick(
                (p.themes_vi as string[]) ?? [],
                (p.themes_en as string[]) ?? (p.themes_vi as string[]) ?? [],
              );
              return (
              <li key={i}>
                <strong>
                  {pick(
                    String(p.working_title_vi ?? p.working_title ?? p.title ?? ""),
                    String(p.working_title ?? p.title ?? p.working_title_vi ?? ""),
                  )}
                </strong>
                <p className="muted tiny">
                  {pick(
                    String(p.focus_vi ?? p.focus ?? ""),
                    String(p.focus_en ?? p.focus ?? p.focus_vi ?? ""),
                  )}
                </p>
                {themes.length > 0 ? (
                  <p className="muted tiny">
                    <strong>{t("pub_themes_h")}: </strong>
                    {themes.join(" · ")}
                  </p>
                ) : null}
              </li>
              );
            })}
          </ul>
        </section>
      ) : null}
      {readiness.length > 0 ? (
        <section className="pub-block">
          <h4>{t("pub_readiness_h")}</h4>
          <ul>
            {readiness.map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
        </section>
      ) : null}
      {rules.length > 0 ? (
        <section className="pub-block pub-integrity">
          <h4>{t("pub_integrity_h")}</h4>
          <ul>
            {rules.map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
        </section>
      ) : null}
    </article>
  );
}

export function OperatingModelView({ data }: { data: unknown }) {
  const { t, pick } = useLocale();
  const r = asRecord(data);
  if (isPublicationManuscript(r)) {
    return (
      <div className="model-ops pub-ops">
        <PublicationManuscriptView data={r} />
      </div>
    );
  }
  if (isAppProduct(r)) {
    return (
      <div className="model-ops pub-ops">
        <AppProductView data={r} />
      </div>
    );
  }
  if (isPracticalApps(r)) {
    return (
      <div className="model-ops pub-ops">
        <PracticalAppsView data={r} />
      </div>
    );
  }
  if (isPublicationPlan(r)) {
    return (
      <div className="model-ops pub-ops">
        <PublicationPlanView data={r} />
      </div>
    );
  }

  const kind = String(r.kind ?? "");
  const isStepOps = kind === "step";
  const caption = pick(
    String(r.caption_vi ?? ""),
    String(r.caption_en ?? r.caption_vi ?? ""),
  );
  const flow = asStringList(
    pick(
      (r.flow_vi as string[] | undefined) ??
        (r.flow as string[] | undefined) ??
        (r.summary_flow as string[] | undefined) ??
        [],
      (r.flow_en as string[] | undefined) ??
        (r.flow as string[] | undefined) ??
        (r.summary_flow as string[] | undefined) ??
        [],
    ),
  );
  const io = asRecord(r.io);
  const ioIn = pick(
    String(io.in_vi ?? io.in ?? ""),
    String(io.in_en ?? io.in ?? ""),
  );
  const ioOut = pick(
    String(io.out_vi ?? io.out ?? ""),
    String(io.out_en ?? io.out ?? ""),
  );
  const actors = asStringList(
    pick(
      (r.actors_vi as string[] | undefined) ??
        (r.actors as string[] | undefined) ??
        (r.modules as string[] | undefined) ??
        [],
      (r.actors_en as string[] | undefined) ??
        (r.actors as string[] | undefined) ??
        (r.modules as string[] | undefined) ??
        [],
    ),
  );
  const archBlock = !isStepOps ? parseArchitectureFromData(r, pick) : null;
  const tilt = useSceneTilt();
  const n = Math.max(flow.length, 1);

  // Step overview: academic workflow list (child tasks) — not the algorithm rail.
  if (isStepOps) {
    return (
      <div className="model-ops ops-step">
        {caption ? <p className="ops-caption-text muted tiny">{caption}</p> : null}
        {flow.length > 0 ? (
          <ol className="ops-step-flow">
            {flow.map((label, i) => (
              <li key={i}>
                <span className="ops-step-idx">{i + 1}</span>
                <span className="ops-step-label">{label}</span>
              </li>
            ))}
          </ol>
        ) : (
          <p className="muted">{t("ops_empty")}</p>
        )}
        {ioIn || ioOut ? (
          <div className="ops-io iso-io">
            <div className="io-card in">
              <strong>{t("ops_in")}</strong>
              <span>{ioIn || "—"}</span>
            </div>
            <div className="io-arrow" aria-hidden>
              ⇒
            </div>
            <div className="io-card out">
              <strong>{t("ops_out")}</strong>
              <span>{ioOut || "—"}</span>
            </div>
          </div>
        ) : null}
        {actors.length > 0 ? (
          <div className="ops-actors">
            {actors.map((a) => (
              <span key={a} className="actor-pill">
                {a}
              </span>
            ))}
          </div>
        ) : null}
      </div>
    );
  }

  return (
    <div className="model-ops ops-algo">
      {caption ? <p className="ops-caption-text muted tiny">{caption}</p> : null}
      {archBlock ? <ArchitectureDiagram block={archBlock} /> : null}
      {!archBlock && flow.length > 0 ? (
        <div
          className={`viz3d ops-3d ${tilt.active ? "is-tilting" : ""}`}
          ref={tilt.ref}
          onPointerMove={tilt.onMove}
          onPointerLeave={tilt.onLeave}
          role="img"
          aria-label={t("ops_caption_algo")}
        >
          <div className="viz3d-hint">{t("math_tilt")}</div>
          <div className="viz3d-stage">
            <div className="viz3d-board ops-board">
              <div className="viz3d-floor rail" aria-hidden />
              <div className="ops-rail" style={{ "--n": n } as CSSProperties}>
                {flow.map((label, i) => (
                  <div
                    key={i}
                    className="iso-block ops-block"
                    style={{ "--i": i } as CSSProperties}
                  >
                    <div className="iso-prism short">
                      <span className="iso-face top" aria-hidden />
                      <span className="iso-face side" aria-hidden />
                      <div className="iso-face front">
                        <span className="iso-idx">{i + 1}</span>
                        <span className="iso-text">{label}</span>
                      </div>
                    </div>
                    {i < flow.length - 1 ? (
                      <div className="iso-pipe horizontal" aria-hidden>
                        <span />
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
          </div>
          <ol className="viz3d-legend horizontal">
            {flow.map((label, i) => (
              <li key={i}>
                <b>{i + 1}</b>
                <span>{label}</span>
              </li>
            ))}
          </ol>
        </div>
      ) : !archBlock ? (
        <p className="muted">{t("ops_empty")}</p>
      ) : null}

      {ioIn || ioOut ? (
        <div className="ops-io iso-io">
          <div className="io-card in">
            <strong>{t("ops_in")}</strong>
            <span>{ioIn || "—"}</span>
          </div>
          <div className="io-arrow" aria-hidden>
            ⇒
          </div>
          <div className="io-card out">
            <strong>{t("ops_out")}</strong>
            <span>{ioOut || "—"}</span>
          </div>
        </div>
      ) : null}

      {actors.length > 0 && !archBlock ? (
        <div className="ops-actors">
          {actors.map((a) => (
            <span key={a} className="actor-pill">
              {a}
            </span>
          ))}
        </div>
      ) : null}
    </div>
  );
}

export function CsdlView({ data }: { data: unknown }) {
  const { t, pick } = useLocale();
  const r = asRecord(data);
  const name = pick(
    String(r.name_vi ?? r.name ?? r.backend ?? "CSDL"),
    String(r.name_en ?? r.name ?? r.backend ?? "Database"),
  );
  const tables = asStringList(
    pick(
      (r.tables_vi as unknown) ?? r.tables ?? r.sources ?? r.features ?? r.metrics ?? r.components ?? [],
      (r.tables_en as unknown) ?? r.tables ?? r.sources ?? r.features ?? r.metrics ?? r.components ?? [],
    ),
  );
  const stores = asStringList(r.stores ?? []);
  const explain = pick(String(r.explain_vi ?? ""), String(r.explain_en ?? ""));
  const role = pick(String(r.role_vi ?? ""), String(r.role_en ?? ""));
  const skip = new Set([
    "name",
    "name_vi",
    "name_en",
    "tables",
    "tables_vi",
    "tables_en",
    "sources",
    "features",
    "metrics",
    "components",
    "stores",
    "backend",
    "explain_vi",
    "explain_en",
    "role_vi",
    "role_en",
  ]);
  const extras = Object.entries(r).filter(([k]) => !skip.has(k));

  return (
    <div className="model-csdl">
      <div className="db-visual" role="img" aria-label="CSDL">
        <svg viewBox="0 0 220 140" className="db-svg">
          <ellipse cx="110" cy="28" rx="70" ry="18" className="db-disk" />
          <path d="M40 28 v70 c0 10 31 18 70 18 s70-8 70-18 V28" className="db-body" />
          <ellipse cx="110" cy="98" rx="70" ry="18" className="db-disk-bottom" />
          <ellipse cx="110" cy="55" rx="70" ry="14" className="db-ring" />
          <ellipse cx="110" cy="78" rx="70" ry="14" className="db-ring" />
          <text x="110" y="34" textAnchor="middle" className="db-caption">
            CSDL
          </text>
        </svg>
        <div className="db-name">{name}</div>
      </div>
      {explain ? (
        <div className="csdl-explain">
          <strong>{t("csdl_explain")}</strong>
          <p>{explain}</p>
        </div>
      ) : null}
      {role ? (
        <div className="csdl-explain role">
          <strong>{t("csdl_role")}</strong>
          <p>{role}</p>
        </div>
      ) : null}
      <div className="db-tables">
        {(tables.length ? tables : stores).map((tbl) => (
          <div key={tbl} className="db-table-card">
            <span className="db-table-ico">▤</span>
            <span>{tbl}</span>
          </div>
        ))}
      </div>
      {extras.length > 0 ? (
        <div className="db-meta">
          {extras.slice(0, 6).map(([k, v]) => (
            <div key={k} className="db-meta-row">
              <strong>{labelize(k)}</strong>
              <span>
                {typeof v === "object" ? summarizeObj(v) : String(v)}
              </span>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function summarizeObj(v: unknown): string {
  if (Array.isArray(v)) return v.map(String).join(", ");
  if (v && typeof v === "object") {
    return Object.entries(v as object)
      .slice(0, 4)
      .map(([k, val]) => `${k}: ${val}`)
      .join(" · ");
  }
  return String(v);
}

export function EvidenceView({ data }: { data: unknown }) {
  const { pick } = useLocale();
  const r = asRecord(data);
  const claim = pick(
    String(r.claim ?? r.claim_vi ?? ""),
    String(r.claim_en ?? r.claim ?? ""),
  );
  const explain = pick(
    String(r.explain_vi ?? r.explain ?? ""),
    String(r.explain_en ?? r.explain ?? ""),
  );
  const logic = pick(
    String(r.logic_vi ?? r.logic ?? ""),
    String(r.logic_en ?? r.logic ?? ""),
  );
  const live = asRecord(r.live);
  const liveSys = asRecord(live.live_system ?? r.live_system);
  const skip = new Set([
    "claim",
    "claim_vi",
    "claim_en",
    "explain",
    "explain_vi",
    "explain_en",
    "logic",
    "logic_vi",
    "logic_en",
    "live",
    "live_system",
    "type",
    "tab",
    "last_run_keys",
    "computed_at_runtime",
    "gaps",
    "sample_ids",
    "viz",
  ]);
  const showGraph = hasResultViz(r);

  return (
    <div className="model-evidence">
      {claim ? <div className="evidence-claim">“{claim}”</div> : null}
      {explain ? <p className="evidence-explain">{explain}</p> : null}
      {logic ? <p className="evidence-logic muted tiny">{logic}</p> : null}
      {showGraph ? <ResultDataViz data={r} /> : null}
      <div className="evidence-stats">
        {Object.entries({ ...r, ...liveSys })
          .filter(
            ([k, v]) =>
              !skip.has(k) &&
              (typeof v === "string" || typeof v === "number" || typeof v === "boolean"),
          )
          .slice(0, 10)
          .map(([k, v]) => {
            let shown = String(v);
            if (typeof v === "number") {
              const ratio =
                /^(faithfulness|hallucination_rate|confidence|p_at_k|r_at_k|mrr|f1|precision|recall|accuracy|score|score_0_1|reliability|freshness|graph_consistency|semantic_relevance)$/i.test(
                  k,
                ) && Math.abs(v) <= 1.0001;
              const alreadyPct = /percent$/i.test(k);
              if (alreadyPct) shown = `${v % 1 === 0 ? v.toFixed(0) : v.toFixed(1)}%`;
              else if (ratio) shown = `${(v * 100).toFixed(1)}%`;
            }
            return (
              <div key={k} className="stat-chip">
                <span>{labelize(k)}</span>
                <strong>{shown}</strong>
              </div>
            );
          })}
      </div>
      {Array.isArray(r.gaps) ? (
        <ul className="plain-list">
          {(r.gaps as string[]).map((g) => (
            <li key={String(g)}>{String(g)}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

/** Prefer language side when backend packed "VI / EN" into one string. */
function localizePacked(text: string, lang: "vi" | "en"): string {
  const parts = text.split(/\s+\/\s+/);
  if (parts.length >= 2) {
    return lang === "en" ? parts[parts.length - 1]! : parts[0]!;
  }
  return text;
}

function assessText(
  r: Record<string, unknown>,
  viKey: string,
  enKey: string,
  lang: "vi" | "en",
): string {
  const vi = r[viKey] != null ? String(r[viKey]) : "";
  const en = r[enKey] != null ? String(r[enKey]) : "";
  if (lang === "en") {
    if (en) return en;
    return localizePacked(vi, "en");
  }
  if (vi) return localizePacked(vi, "vi");
  return en;
}

export function AssessmentView({ data }: { data: unknown }) {
  const { t, lang, pick } = useLocale();
  const r = asRecord(data);
  const score = typeof r.score_0_1 === "number" ? r.score_0_1 : null;
  const pct = score != null ? Math.round(score * 100) : null;
  const strength = assessText(r, "strength", "strength_en", lang);
  let limitation = assessText(r, "limitation", "limitation_en", lang);
  // Rewrite stale cached copy of the old passive limitation note
  if (
    /chưa thay thế thẩm định|đánh giá tự động trên demo|không lặp ở đây|not a substitute for expert|automatic demo assessment/i.test(
      limitation,
    )
  ) {
    limitation = t("assess_limitation_scientific");
  }
  const verdict = assessText(r, "verdict", "verdict_en", lang);
  const verifyStatus = String(r.verification_status ?? "");
  const expertStatus = String(r.expert_status ?? "");
  const bridge = pick(
    String(r.scientific_bridge_vi ?? ""),
    String(r.scientific_bridge_en ?? r.scientific_bridge_vi ?? ""),
  );
  const evidence = asStringList(
    pick(
      (r.evidence_vi as unknown) ?? [],
      (r.evidence_en as unknown) ?? r.evidence_vi ?? [],
    ),
  );
  const figures = asStringList(
    pick(
      (r.figures_vi as unknown) ?? [],
      (r.figures_en as unknown) ?? r.figures_vi ?? [],
    ),
  );
  const support = asStringList(
    pick(
      (r.support_vi as unknown) ?? [],
      (r.support_en as unknown) ?? r.support_vi ?? [],
    ),
  );
  const citations = Array.isArray(r.citations)
    ? (r.citations as Array<Record<string, unknown> | string>)
    : [];

  const hasSupport =
    evidence.length > 0 ||
    figures.length > 0 ||
    citations.length > 0 ||
    support.length > 0;

  const evidenceProse = evidence.filter((x) => !isAssessMetricLine(x));
  const evidenceMetrics = evidence.filter((x) => isAssessMetricLine(x));
  const supportCols =
    (evidence.length > 0 ? 1 : 0) +
    (figures.length > 0 ? 1 : 0) +
    (citations.length > 0 ? 1 : 0);

  return (
    <div className="model-assess">
      {verifyStatus || expertStatus || bridge ? (
        <div className="assess-verify-strip">
          {verifyStatus ? (
            <span className={`sci-verify-badge ${verifyStatus}`}>
              {verifyStatus === "verified"
                ? t("sci_verify_badge_verified")
                : verifyStatus === "partial"
                  ? t("sci_verify_badge_partial")
                  : verifyStatus === "weak"
                    ? t("sci_verify_badge_weak")
                    : t("sci_verify_badge_pending")}
            </span>
          ) : null}
          {expertStatus ? (
            <span className="assess-expert-chip muted tiny">
              {t("sci_verify_expert")}: {expertStatus}
            </span>
          ) : null}
          {bridge ? <p className="muted tiny assess-bridge">{bridge}</p> : null}
        </div>
      ) : null}
      <div className="assess-top">
        {pct != null ? (
          <div
            className="gauge-wrap"
            role="img"
            aria-label={`${t("acad_score_title")} ${pct}`}
          >
            <svg viewBox="0 0 120 70" className="gauge-svg">
              <path
                d="M10 60 A50 50 0 0 1 110 60"
                className="gauge-bg"
              />
              <path
                d="M10 60 A50 50 0 0 1 110 60"
                className="gauge-fg"
                style={{
                  strokeDasharray: `${(pct / 100) * 157} 157`,
                }}
              />
              <text x="60" y="58" textAnchor="middle" className="gauge-text">
                {pct}%
              </text>
            </svg>
            <span className="gauge-caption muted tiny">{t("acad_score_title")}</span>
          </div>
        ) : null}
        <div className="assess-grid">
          {strength ? (
            <div className="assess-card good">
              <strong>{t("assess_strength")}</strong>
              <p>{strength}</p>
            </div>
          ) : null}
          {limitation ? (
            <div className="assess-card warn">
              <strong>{t("assess_limitation")}</strong>
              <p>{limitation}</p>
            </div>
          ) : null}
          {verdict ? (
            <div className="assess-card verdict">
              <strong>{t("assess_verdict")}</strong>
              <p>{verdict}</p>
            </div>
          ) : null}
        </div>
      </div>

      {hasSupport ? (
        <div className="assess-support">
          <div className="assess-support-head">
            <h5 className="assess-support-title">{t("assess_support_h")}</h5>
            {support.length > 0 ? (
              <div className="assess-support-tips">
                {support.map((x, i) => (
                  <span key={`s-${i}`} className="assess-tip-chip">
                    {x}
                  </span>
                ))}
              </div>
            ) : null}
          </div>
          <div
            className={`assess-support-grid cols-${Math.max(1, Math.min(3, supportCols))}`}
          >
            {evidence.length > 0 ? (
              <div className="assess-support-block">
                <strong>{t("assess_evidence_h")}</strong>
                {evidenceProse.length > 0 ? (
                  <ul className="assess-prose-list">
                    {evidenceProse.map((x, i) => (
                      <li key={`e-${i}`}>{x}</li>
                    ))}
                  </ul>
                ) : null}
                {evidenceMetrics.length > 0 ? (
                  <div className="assess-metric-chips">
                    {evidenceMetrics.map((x, i) => (
                      <span key={`m-${i}`} className="assess-metric-chip mono">
                        {x.replace(/^Live\s+/i, "").replace(/\s*·\s*/g, " · ")}
                      </span>
                    ))}
                  </div>
                ) : null}
              </div>
            ) : null}
            {figures.length > 0 ? (
              <div className="assess-support-block">
                <strong>{t("assess_figures_h")}</strong>
                <ul className="assess-prose-list">
                  {figures.map((x, i) => (
                    <li key={`f-${i}`}>{x}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            {citations.length > 0 ? (
              <div className="assess-support-block">
                <strong>{t("assess_cites_h")}</strong>
                <ol className="assess-cite-list">
                  {citations.map((c, i) => {
                    if (typeof c === "string") {
                      return <li key={i}>{c}</li>;
                    }
                    const text = String(c.text ?? "");
                    const doi = c.doi != null ? String(c.doi) : "";
                    return (
                      <li key={String(c.id ?? i)}>
                        <span>{text}</span>
                        {doi ? (
                          <span className="mono tiny"> — DOI/Ref: {doi}</span>
                        ) : null}
                      </li>
                    );
                  })}
                </ol>
              </div>
            ) : null}
          </div>
        </div>
      ) : null}
    </div>
  );
}

/** Metric/key-value lines for assessment chips (avoid KaTeX on |P|, type=…). */
function isAssessMetricLine(s: string): boolean {
  const t = s.trim();
  if (!t) return false;
  if (/^(metric|axes|type|gaps|paper|chapter|task|Live)\b/i.test(t)) return true;
  if (/^[a-zA-Z_][\w.]*\s*[:=·]/.test(t) && t.length < 80) return true;
  if (/\b=\s*\d/.test(t) && t.length < 60) return true;
  return false;
}

export function CitationsView({ data }: { data: unknown }): ReactNode {
  const { t } = useLocale();
  if (!Array.isArray(data) || !data.length)
    return <span className="muted">{t("cite_empty")}</span>;
  return (
    <ol className="cite-list">
      {(data as Array<{ text: string; doi?: string; id?: string }>).map((c, i) => (
        <li key={c.id ?? i}>
          <div>{c.text}</div>
          {c.doi ? <div className="mono tiny">DOI/Ref: {c.doi}</div> : null}
        </li>
      ))}
    </ol>
  );
}
