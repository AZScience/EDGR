import {
  useEffect,
  useRef,
  useState,
  type CSSProperties,
} from "react";
import type { PipelineDefinition, TaskResult } from "./api";
import type { MessageKey } from "./i18n/messages";
import { STEP_COLORS, StepIcon } from "./StepIcon";

type PickFn = (vi: string, en: string) => string;
type TFn = (key: MessageKey, vars?: Record<string, string | number>) => string;

type Props = {
  stepId: number;
  setStepId: (id: number) => void;
  def: PipelineDefinition | null;
  cache: Record<string, TaskResult>;
  pick: PickFn;
  t: TFn;
};

export function StepRail({ stepId, setStepId, def, cache, pick, t }: Props) {
  const trackRef = useRef<HTMLDivElement>(null);
  const [canPrev, setCanPrev] = useState(false);
  const [canNext, setCanNext] = useState(false);

  const updateArrows = () => {
    const el = trackRef.current;
    if (!el) return;
    const { scrollLeft, scrollWidth, clientWidth } = el;
    setCanPrev(scrollLeft > 4);
    setCanNext(scrollLeft + clientWidth < scrollWidth - 4);
  };

  useEffect(() => {
    updateArrows();
    const el = trackRef.current;
    if (!el) return;
    const onScroll = () => updateArrows();
    el.addEventListener("scroll", onScroll, { passive: true });
    const ro = new ResizeObserver(updateArrows);
    ro.observe(el);
    window.addEventListener("resize", updateArrows);
    return () => {
      el.removeEventListener("scroll", onScroll);
      ro.disconnect();
      window.removeEventListener("resize", updateArrows);
    };
  }, [def?.steps.length]);

  useEffect(() => {
    const el = trackRef.current;
    if (!el) return;
    const active = el.querySelector<HTMLElement>(".step-chip.active");
    active?.scrollIntoView({
      behavior: "smooth",
      inline: "center",
      block: "nearest",
    });
    const timer = window.setTimeout(updateArrows, 380);
    return () => clearTimeout(timer);
  }, [stepId, def?.steps.length]);

  const scrollByDir = (dir: -1 | 1) => {
    const el = trackRef.current;
    if (!el) return;
    const amount = Math.max(Math.round(el.clientWidth * 0.7), 240);
    el.scrollBy({ left: dir * amount, behavior: "smooth" });
  };

  return (
    <div className="step-rail-wrap">
      <button
        type="button"
        className="step-rail-arrow"
        disabled={!canPrev}
        onClick={() => scrollByDir(-1)}
        aria-label={t("rail_prev")}
        title={t("rail_prev")}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden>
          <path
            d="M15 6l-6 6 6 6"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      <nav
        ref={trackRef}
        className="step-rail"
        aria-label={t("rail_aria")}
      >
        <button
          type="button"
          className={`step-chip overview-chip ${stepId === 0 ? "active" : ""}`}
          onClick={() => setStepId(0)}
          title={t("overview_tab")}
          style={{ "--step-color": STEP_COLORS[0] } as CSSProperties}
        >
          <span className="chip-head">
            <span
              className="icon-wrap"
              style={{
                background: `${STEP_COLORS[0]}18`,
                borderColor: `${STEP_COLORS[0]}55`,
              }}
            >
              <StepIcon stepId={0} size={20} />
            </span>
            <span className="num" style={{ color: STEP_COLORS[0] }}>
              0
            </span>
          </span>
          <span className="label">{t("overview_tab")}</span>
        </button>

        {def?.steps.map((s) => {
          const done = s.tasks.every((task) => cache[`${s.id}:${task.id}`]);
          const partial = s.tasks.some((task) => cache[`${s.id}:${task.id}`]);
          const color = STEP_COLORS[s.id] ?? "#0D7377";
          const stepTitle = pick(s.title, s.title_en);
          return (
            <button
              key={s.id}
              type="button"
              className={`step-chip ${stepId === s.id ? "active" : ""} ${done ? "done" : partial ? "partial" : ""}`}
              onClick={() => setStepId(s.id)}
              title={stepTitle}
              style={{ "--step-color": color } as CSSProperties}
            >
              <span className="chip-head">
                <span
                  className="icon-wrap"
                  style={{ background: `${color}18`, borderColor: `${color}55` }}
                >
                  <StepIcon stepId={s.id} size={20} />
                </span>
                <span className="num" style={{ color }}>
                  {s.id}
                </span>
              </span>
              <span className="label">{stepTitle}</span>
              {s.badge || s.badge_en ? (
                <span className="mini-badge">
                  {pick(
                    s.badge ?? s.badge_en ?? "",
                    s.badge_en ?? s.badge ?? "",
                  )}
                </span>
              ) : null}
            </button>
          );
        })}
      </nav>

      <button
        type="button"
        className="step-rail-arrow"
        disabled={!canNext}
        onClick={() => scrollByDir(1)}
        aria-label={t("rail_next")}
        title={t("rail_next")}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden>
          <path
            d="M9 6l6 6-6 6"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>
    </div>
  );
}
