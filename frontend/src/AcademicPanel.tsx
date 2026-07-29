import type { CSSProperties, ReactNode } from "react";
import type { AcademicPackage } from "./api";
import { useLocale } from "./i18n/LocaleContext";
import type { MessageKey } from "./i18n/messages";
import { ResultDataViz } from "./DataViz";
import { MathText } from "./mathFormat";
import {
  AlgorithmModelView,
  AssessmentView,
  CitationsView,
  CsdlView,
  EvidenceView,
  MathModelView,
  OperatingModelView,
} from "./modelViews";

/** Document order for thesis/copy — not a dashboard grid. */
const DOC_BLOCK_ORDER: Array<{
  key: keyof AcademicPackage["blocks"];
  titleKey: MessageKey;
  subKey: MessageKey;
  anchor: string;
}> = [
  {
    key: "csdl",
    titleKey: "block_csdl",
    subKey: "block_csdl_sub",
    anchor: "sci-csdl",
  },
  {
    key: "mo_hinh_toan",
    titleKey: "block_math_full",
    subKey: "block_math_sub_full",
    anchor: "sci-math",
  },
  {
    key: "mo_hinh_thuat_toan",
    titleKey: "block_algo_full",
    subKey: "block_algo_sub_full",
    anchor: "sci-algo",
  },
  {
    key: "mo_hinh_hoat_dong",
    titleKey: "block_ops",
    subKey: "block_ops_sub",
    anchor: "sci-ops",
  },
  {
    key: "trich_dan",
    titleKey: "block_cite",
    subKey: "block_cite_sub",
    anchor: "sci-cite",
  },
  {
    key: "minh_chung",
    titleKey: "block_ev",
    subKey: "block_ev_sub_full",
    anchor: "sci-ev",
  },
  {
    key: "nhan_dinh_danh_gia",
    titleKey: "result_assess_design_h",
    subKey: "block_assess_sub",
    anchor: "sci-assess",
  },
];

function BlockBody({
  blockKey,
  data,
}: {
  blockKey: keyof AcademicPackage["blocks"];
  data: unknown;
}) {
  switch (blockKey) {
    case "csdl":
      return <CsdlView data={data} />;
    case "mo_hinh_toan":
      return <MathModelView data={data} />;
    case "mo_hinh_thuat_toan":
      return <AlgorithmModelView data={data} />;
    case "mo_hinh_hoat_dong":
      return <OperatingModelView data={data} />;
    case "trich_dan":
      return <CitationsView data={data} />;
    case "minh_chung":
      return <EvidenceView data={data} />;
    case "nhan_dinh_danh_gia":
      return <AssessmentView data={data} />;
    default:
      return <span className="muted">—</span>;
  }
}

function DocSection({
  id,
  num,
  title,
  subtitle,
  children,
}: {
  id: string;
  num: number;
  title: string;
  subtitle?: string;
  children: ReactNode;
}) {
  return (
    <section id={id} className="doc-section surface" data-doc-num={num}>
      <header className="doc-section-head">
        <h4>
          <span className="sci-step-num">{num}</span>
          {title}
        </h4>
        {subtitle ? <p className="doc-section-sub">{subtitle}</p> : null}
      </header>
      <div className="doc-section-body">{children}</div>
    </section>
  );
}

export function AcademicPanel({
  pack,
  color,
  loading,
  hideBlocks,
}: {
  pack: AcademicPackage | null;
  color: string;
  loading?: boolean;
  /** Block keys to omit (e.g. hide static assessment when runtime review owns it). */
  hideBlocks?: Array<keyof AcademicPackage["blocks"]>;
}) {
  const { t, pick } = useLocale();

  if (loading) {
    return (
      <div className="academic-panel">
        <p className="muted">{t("acad_loading")}</p>
      </div>
    );
  }
  if (!pack) {
    return (
      <div className="academic-panel">
        <p className="muted">{t("acad_empty")}</p>
      </div>
    );
  }

  const omitted = new Set(hideBlocks ?? []);
  const showAssess = !omitted.has("nhan_dinh_danh_gia");
  const score = showAssess
    ? pack.blocks.nhan_dinh_danh_gia?.score_0_1
    : undefined;
  const purpose = pack.purpose;
  const purposeText = purpose
    ? pick(purpose.vi ?? "", purpose.en ?? "")
    : "";
  const doesText = purpose
    ? pick(purpose.does_vi ?? "", purpose.does_en ?? "")
    : "";
  const theory = pack.theory;
  const panelTitle = pick(pack.title, pack.title_en ?? pack.title);
  const theoryName = theory
    ? pick(theory.name_vi ?? "", theory.name_en ?? "")
    : "";
  const showTheoryName =
    !!theoryName &&
    theoryName.trim().toLowerCase() !== panelTitle.trim().toLowerCase();
  const theoryWhat = theory
    ? pick(theory.what_vi ?? "", theory.what_en ?? "")
    : "";
  const theoryWhy = theory
    ? pick(theory.why_vi ?? "", theory.why_en ?? "")
    : "";
  const theoryIdeas = theory
    ? pick(theory.ideas_vi ?? [], theory.ideas_en ?? [])
    : [];
  const theoryRefs = theory?.refs ?? "";
  const theoryArgument = theory
    ? pick(theory.argument_vi ?? "", theory.argument_en ?? "")
    : "";
  const theoryAssumptions = theory
    ? pick(theory.assumptions_vi ?? [], theory.assumptions_en ?? [])
    : [];
  const theoryFrame = theory
    ? pick(theory.frame_vi ?? "", theory.frame_en ?? "")
    : "";
  const theoryScope = theory
    ? pick(theory.scope_vi ?? "", theory.scope_en ?? "")
    : "";
  const theoryIntro = theory
    ? pick(theory.intro_vi ?? "", theory.intro_en ?? "")
    : "";
  const theoryChildTabs = (theory?.child_tabs ?? []).map((ct) => ({
    id: ct.id ?? "",
    index: ct.index ?? 0,
    title: pick(ct.title_vi ?? "", ct.title_en ?? ct.title_vi ?? ""),
    blurb: pick(ct.blurb_vi ?? "", ct.blurb_en ?? ct.blurb_vi ?? ""),
  }));
  const theoryRelated = (theory?.related_work ?? []).map((rw) => ({
    cite: rw.cite ?? "",
    role: pick(rw.role_vi ?? "", rw.role_en ?? ""),
  }));

  const rawSequence = pick(
    pack.scientific_sequence_vi ?? [],
    pack.scientific_sequence_en ?? pack.scientific_sequence_vi ?? [],
  );
  const sequence = rawSequence.map((item, i) => {
    if (typeof item === "string") {
      return { id: `step-${i}`, title: item, explain: "", anchor: "" };
    }
    return {
      id: item.id || `step-${i}`,
      title: pick(item.title_vi || "", item.title_en || item.title_vi || ""),
      explain: pick(
        item.explain_vi || "",
        item.explain_en || item.explain_vi || "",
      ),
      anchor: item.anchor || "",
    };
  });

  const hasTheory = !!(
    theoryIntro ||
    theoryChildTabs.length ||
    theoryWhat ||
    theoryWhy ||
    theoryIdeas.length ||
    theoryArgument ||
    theoryAssumptions.length
  );
  const hasPurpose = !!(purposeText || doesText);
  const hasGraph = !!(
    pack.graph_preview?.nodes && pack.graph_preview.nodes.length > 0
  );

  const docBlocks = DOC_BLOCK_ORDER.filter((b) => !omitted.has(b.key));

  // Continuous section numbers for copy-ready document
  let n = 0;
  const next = () => {
    n += 1;
    return n;
  };
  const numTheory = hasTheory ? next() : 0;
  const numPurpose = hasPurpose ? next() : 0;
  const numCsdl = !omitted.has("csdl") ? next() : 0;
  const numMath = !omitted.has("mo_hinh_toan") ? next() : 0;
  const numAlgo = !omitted.has("mo_hinh_thuat_toan") ? next() : 0;
  const numOps = !omitted.has("mo_hinh_hoat_dong") ? next() : 0;
  const numCite = !omitted.has("trich_dan") ? next() : 0;
  const numGraph = hasGraph ? next() : 0;
  const numEv = !omitted.has("minh_chung") ? next() : 0;
  const numAssess =
    showAssess && !omitted.has("nhan_dinh_danh_gia") ? next() : 0;

  const blockNum: Partial<Record<keyof AcademicPackage["blocks"], number>> = {
    csdl: numCsdl,
    mo_hinh_toan: numMath,
    mo_hinh_thuat_toan: numAlgo,
    mo_hinh_hoat_dong: numOps,
    trich_dan: numCite,
    minh_chung: numEv,
    nhan_dinh_danh_gia: numAssess,
  };

  return (
    <div
      className="academic-panel academic-doc"
      style={{ "--step-color": color } as CSSProperties}
    >
      <header className="academic-head">
        <div>
          <div className="academic-scope">
            {pack.scope === "step"
              ? t("acad_scope_step")
              : t("acad_scope_task")}
          </div>
          <h3>{panelTitle}</h3>
          <p className="doc-copy-hint muted tiny">{t("doc_copy_hint")}</p>
        </div>
        {typeof score === "number" ? (
          <div className="assess-score" title={t("acad_score_title")}>
            {(score * 100).toFixed(0)}
            <small>%</small>
          </div>
        ) : null}
      </header>

      {sequence.length > 0 ? (
        <nav className="sci-sequence surface" aria-label={t("sci_seq_h")}>
          <h4>{t("sci_seq_h")}</h4>
          <p className="sci-sequence-lead muted tiny">{t("sci_seq_lead")}</p>
          <ol className="sci-roadmap">
            {sequence.map((item, i) => (
              <li key={item.id}>
                <div className="sci-roadmap-head">
                  <span className="sci-step-num">{i + 1}</span>
                  {item.anchor ? (
                    <a href={`#${item.anchor}`} className="sci-roadmap-title">
                      {item.title}
                    </a>
                  ) : (
                    <strong className="sci-roadmap-title">{item.title}</strong>
                  )}
                </div>
                {item.explain ? (
                  <p className="sci-roadmap-explain">{item.explain}</p>
                ) : null}
              </li>
            ))}
          </ol>
        </nav>
      ) : (
        <p className="scientific-frame-note muted tiny">{t("scientific_frame_h")}</p>
      )}

      <div className="academic-doc-stack">
        {(() => {
          const theoryBody = (
            <div className="theory-academic">
              {theoryFrame ? (
                <p className="theory-frame muted tiny">{theoryFrame}</p>
              ) : null}
              {showTheoryName ? (
                <p className="theory-name">{theoryName}</p>
              ) : null}
              {theoryScope ? (
                <p className="theory-scope muted tiny">
                  <strong>{t("theory_scope")}: </strong>
                  {theoryScope}
                </p>
              ) : null}
              {theoryIntro ? (
                <div className="theory-block theory-intro">
                  <strong>{t("theory_intro")}</strong>
                  <MathText text={theoryIntro} as="p" />
                </div>
              ) : null}
              {theoryChildTabs.length > 0 ? (
                <div
                  id="sci-theory-tabs"
                  className="theory-block theory-child-tabs"
                >
                  <strong>{t("theory_child_tabs")}</strong>
                  <ol className="theory-child-tabs-list">
                    {theoryChildTabs.map((ct) => (
                      <li key={ct.id || ct.title}>
                        <span className="theory-child-tab-title">
                          {ct.index ? `${ct.index}. ` : ""}
                          {ct.title}
                        </span>
                        {ct.blurb ? (
                          <MathText
                            text={ct.blurb}
                            as="p"
                            className="theory-child-tab-blurb muted"
                          />
                        ) : null}
                      </li>
                    ))}
                  </ol>
                </div>
              ) : null}
              {theoryWhat ? (
                <div className="theory-block">
                  <strong>{t("theory_what")}</strong>
                  <MathText text={theoryWhat} as="p" />
                </div>
              ) : null}
              {theoryAssumptions.length > 0 ? (
                <div className="theory-block theory-assumptions">
                  <strong>{t("theory_assumptions")}</strong>
                  <ol>
                    {theoryAssumptions.map((a, i) => (
                      <MathText key={i} text={a} as="li" />
                    ))}
                  </ol>
                </div>
              ) : null}
              {theoryWhy ? (
                <div className="theory-block">
                  <strong>{t("theory_why")}</strong>
                  <MathText text={theoryWhy} as="p" />
                </div>
              ) : null}
              {theoryArgument ? (
                <div className="theory-block theory-argument">
                  <strong>{t("theory_argument")}</strong>
                  <MathText text={theoryArgument} as="p" />
                </div>
              ) : null}
              {theoryIdeas.length > 0 ? (
                <div className="theory-block">
                  <strong>{t("theory_ideas")}</strong>
                  <ul>
                    {theoryIdeas.map((idea, i) => (
                      <MathText key={i} text={idea} as="li" />
                    ))}
                  </ul>
                </div>
              ) : null}
              {theoryRelated.length > 0 ? (
                <div className="theory-block theory-related">
                  <strong>{t("theory_related")}</strong>
                  <ul className="theory-related-list">
                    {theoryRelated.map((rw, i) =>
                      rw.cite ? (
                        <li key={i}>
                          <cite>{rw.cite}</cite>
                          {rw.role ? (
                            <span className="muted"> — {rw.role}</span>
                          ) : null}
                        </li>
                      ) : null,
                    )}
                  </ul>
                </div>
              ) : theoryRefs ? (
                <p className="theory-refs muted tiny">
                  <strong>{t("theory_refs")}: </strong>
                  {theoryRefs}
                </p>
              ) : null}
            </div>
          );
          const purposeBody = (
            <>
              {purposeText ? <p>{purposeText}</p> : null}
              {doesText ? (
                <p>
                  <strong>{t("purpose_does")}</strong> {doesText}
                </p>
              ) : null}
            </>
          );
          // Theory is full-width (scholarly reading); purpose follows as its own section.
          return (
            <>
              {hasTheory ? (
                <DocSection
                  id="sci-theory"
                  num={numTheory}
                  title={t("theory_h")}
                  subtitle={t("doc_sec_theory_sub")}
                >
                  {theoryBody}
                </DocSection>
              ) : null}
              {hasPurpose ? (
                <DocSection
                  id="sci-purpose"
                  num={numPurpose}
                  title={t("purpose_h")}
                  subtitle={t("doc_sec_purpose_sub")}
                >
                  {purposeBody}
                </DocSection>
              ) : null}
            </>
          );
        })()}

        {(() => {
          /** Left → right pairs on one row (2 columns). */
          const PAIR_WITH: Partial<
            Record<keyof AcademicPackage["blocks"], keyof AcademicPackage["blocks"]>
          > = {
            csdl: "mo_hinh_toan",
            mo_hinh_thuat_toan: "mo_hinh_hoat_dong",
            trich_dan: "minh_chung",
          };
          const consumed = new Set<keyof AcademicPackage["blocks"]>();
          const nodes: ReactNode[] = [];

          for (const b of docBlocks) {
            if (consumed.has(b.key)) continue;
            const num = blockNum[b.key] || 0;
            if (!num) continue;

            const rightKey = PAIR_WITH[b.key];
            const rightMeta = rightKey
              ? docBlocks.find((x) => x.key === rightKey)
              : undefined;
            const rightNum = rightKey ? blockNum[rightKey] || 0 : 0;
            const willPair = !!(rightMeta && rightNum > 0);

            // Graph sits full-width just above Evidence (or the Cite|Evidence pair)
            const insertGraph =
              hasGraph &&
              numGraph > 0 &&
              ((b.key === "minh_chung" && !willPair) ||
                (b.key === "trich_dan" && willPair && rightKey === "minh_chung"));
            if (insertGraph) {
              nodes.push(
                <DocSection
                  key="sci-graph"
                  id="sci-graph"
                  num={numGraph}
                  title={t("graph_preview_h")}
                  subtitle={t("graph_preview_hint")}
                >
                  <ResultDataViz data={{ viz: pack.graph_preview }} />
                </DocSection>,
              );
            }

            if (willPair && rightMeta) {
              consumed.add(rightMeta.key);
              const leftTitle =
                b.key === "mo_hinh_hoat_dong"
                  ? t(pack.scope === "step" ? "block_ops_step" : "block_ops_algo")
                  : t(b.titleKey);
              const leftSub =
                b.key === "mo_hinh_hoat_dong"
                  ? t(
                      pack.scope === "step"
                        ? "block_ops_step_sub"
                        : "block_ops_algo_sub",
                    )
                  : t(b.subKey);
              const rightTitle =
                rightMeta.key === "mo_hinh_hoat_dong"
                  ? t(pack.scope === "step" ? "block_ops_step" : "block_ops_algo")
                  : t(rightMeta.titleKey);
              const rightSub =
                rightMeta.key === "mo_hinh_hoat_dong"
                  ? t(
                      pack.scope === "step"
                        ? "block_ops_step_sub"
                        : "block_ops_algo_sub",
                    )
                  : t(rightMeta.subKey);
              nodes.push(
                <div key={`${b.key}-${rightMeta.key}-row`} className="doc-pair-row">
                  <DocSection
                    id={b.anchor}
                    num={num}
                    title={leftTitle}
                    subtitle={leftSub}
                  >
                    <BlockBody blockKey={b.key} data={pack.blocks[b.key]} />
                  </DocSection>
                  <DocSection
                    id={rightMeta.anchor}
                    num={rightNum}
                    title={rightTitle}
                    subtitle={rightSub}
                  >
                    <BlockBody
                      blockKey={rightMeta.key}
                      data={pack.blocks[rightMeta.key]}
                    />
                  </DocSection>
                </div>,
              );
              continue;
            }

            const soloTitle =
              b.key === "mo_hinh_hoat_dong"
                ? t(pack.scope === "step" ? "block_ops_step" : "block_ops_algo")
                : t(b.titleKey);
            const soloSub =
              b.key === "mo_hinh_hoat_dong"
                ? t(
                    pack.scope === "step"
                      ? "block_ops_step_sub"
                      : "block_ops_algo_sub",
                  )
                : t(b.subKey);
            nodes.push(
              <DocSection
                key={b.key}
                id={b.anchor}
                num={num}
                title={soloTitle}
                subtitle={soloSub}
              >
                <BlockBody blockKey={b.key} data={pack.blocks[b.key]} />
              </DocSection>,
            );
          }
          return nodes;
        })()}

        {/* Graph-only tabs with no minh_chung visible still need the figure */}
        {hasGraph &&
        (omitted.has("minh_chung") || !blockNum.minh_chung) ? (
          <DocSection
            id="sci-graph"
            num={numGraph}
            title={t("graph_preview_h")}
            subtitle={t("graph_preview_hint")}
          >
            <ResultDataViz data={{ viz: pack.graph_preview }} />
          </DocSection>
        ) : null}
      </div>

      <p className="doc-runtime-bridge muted tiny">{t("doc_runtime_bridge")}</p>
    </div>
  );
}
