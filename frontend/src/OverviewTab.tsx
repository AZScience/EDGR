import type { CSSProperties } from "react";
import { useLocale } from "./i18n/LocaleContext";
import type { MessageKey } from "./i18n/messages";
import { STEP_COLORS, StepIcon } from "./StepIcon";

const PHASES: Array<{
  titleKey: MessageKey;
  rangeKey: MessageKey;
  color: string;
  itemKeys: MessageKey[];
}> = [
  {
    titleKey: "phase1_title",
    rangeKey: "phase1_range",
    color: "#2563EB",
    itemKeys: [
      "phase1_i1",
      "phase1_i2",
      "phase1_i3",
      "phase1_i4",
      "phase1_i5",
      "phase1_i6",
    ],
  },
  {
    titleKey: "phase2_title",
    rangeKey: "phase2_range",
    color: "#0D9488",
    itemKeys: [
      "phase2_i1",
      "phase2_i2",
      "phase2_i3",
      "phase2_i4",
      "phase2_i5",
    ],
  },
  {
    titleKey: "phase3_title",
    rangeKey: "phase3_range",
    color: "#CA8A04",
    itemKeys: ["phase3_i1", "phase3_i2", "phase3_i3", "phase3_i4", "phase3_i5"],
  },
];

const FLOW_KEYS: MessageKey[] = [
  "overview_flow_1",
  "overview_flow_2",
  "overview_flow_3",
  "overview_flow_4",
  "overview_flow_5",
  "overview_flow_6",
  "overview_flow_7",
  "overview_flow_8",
  "overview_flow_9",
];

type Props = {
  topic?: string;
  topicVi?: string;
  onGoStep: (id: number) => void;
};

export function OverviewTab({ topic, topicVi, onGoStep }: Props) {
  const { t, pick, lang } = useLocale();
  const processImg =
    lang === "en" ? "/quy-trinh-a-z-en.png" : "/quy-trinh-a-z.png";

  return (
    <section className="panel overview-tab">
      <div className="section-head">
        <h2 className="step-title-row">
          <span
            className="step-title-icon"
            style={{
              background: `${STEP_COLORS[0]}18`,
              borderColor: `${STEP_COLORS[0]}55`,
            }}
          >
            <StepIcon stepId={0} size={28} />
          </span>
          <span>{t("overview_tab_title")}</span>
        </h2>
        <p>
          {pick(
            topicVi ??
              "Thuật toán truy hồi đồ thị động dựa trên bằng chứng để giảm ảo giác LLM trong IDS và CTI.",
            topic ??
              "Evidence-driven dynamic graph retrieval to mitigate LLM hallucination in IDS and CTI.",
          )}
        </p>
      </div>

      <div className="overview-hero-card">
        <img
          key={processImg}
          src={processImg}
          alt={t("overview_img_alt")}
          className="overview-image"
        />
      </div>

      <div className="overview-explain surface">
        <h3>{t("overview_explain_h")}</h3>
        <p>{t("overview_explain_p1")}</p>
        <p>{t("overview_explain_p2")}</p>
      </div>

      <div className="overview-phases">
        {PHASES.map((p) => (
          <article
            key={p.titleKey}
            className="surface phase-card"
            style={{ "--phase": p.color } as CSSProperties}
          >
            <header>
              <strong>{t(p.titleKey)}</strong>
              <span>{t(p.rangeKey)}</span>
            </header>
            <ul>
              {p.itemKeys.map((k) => (
                <li key={k}>{t(k)}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>

      <div className="surface overview-flow">
        <h3>{t("overview_flow_h")}</h3>
        <div className="flow-line">
          {FLOW_KEYS.map((k, i) => (
            <span key={k} className="flow-node">
              {t(k)}
              {i < FLOW_KEYS.length - 1 ? <i>→</i> : null}
            </span>
          ))}
        </div>
      </div>

      <div className="surface overview-jump">
        <h3>{t("overview_jump_h")}</h3>
        <div className="jump-grid">
          {Array.from({ length: 16 }, (_, i) => i + 1).map((id) => (
            <button
              key={id}
              className="jump-btn"
              style={{ "--step-color": STEP_COLORS[id] } as CSSProperties}
              onClick={() => onGoStep(id)}
            >
              <StepIcon stepId={id} size={18} />
              <span>{t("overview_step_btn", { id })}</span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
