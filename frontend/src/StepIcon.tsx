/** Colored SVG icons for the research pipeline steps. */

export const STEP_COLORS: Record<number, string> = {
  0: "#0F766E", // overview — deep teal
  1: "#2563EB", // literature — blue
  2: "#EA580C", // gaps — orange
  3: "#0D9488", // problem — teal
  4: "#16A34A", // edgr — green
  5: "#7C3AED", // dkg — violet
  6: "#DC2626", // scoring — red
  7: "#0891B2", // data — cyan
  8: "#4338CA", // system — indigo
  9: "#D97706", // experiments — amber
  10: "#059669", // evaluation — emerald
  11: "#DB2777", // ablation — pink
  12: "#475569", // analysis — slate
  13: "#0284C7", // publication — sky
  14: "#B45309", // dissertation — brown/amber
  15: "#CA8A04", // defense — gold
  16: "#0F766E", // practical app — deep teal
};

type Props = {
  stepId: number;
  size?: number;
  className?: string;
};

export function StepIcon({ stepId, size = 22, className = "" }: Props) {
  const color = STEP_COLORS[stepId] ?? "#0D7377";
  const common = {
    width: size,
    height: size,
    viewBox: "0 0 24 24",
    fill: "none",
    xmlns: "http://www.w3.org/2000/svg",
    className,
    "aria-hidden": true as const,
  };

  switch (stepId) {
    case 0: // overview map
      return (
        <svg {...common}>
          <rect x="3" y="4" width="18" height="16" rx="2" fill={`${color}22`} stroke={color} strokeWidth="1.6" />
          <path d="M7 8h4M7 12h10M7 16h7" stroke={color} strokeWidth="1.8" strokeLinecap="round" />
          <circle cx="17" cy="8" r="2.2" fill={color} />
        </svg>
      );
    case 1: // book
      return (
        <svg {...common}>
          <rect x="3" y="4" width="18" height="16" rx="2" fill={color} opacity="0.2" />
          <path d="M4 5.5A1.5 1.5 0 0 1 5.5 4H12v16H5.5A1.5 1.5 0 0 1 4 18.5v-13Z" fill={color} />
          <path d="M12 4h6.5A1.5 1.5 0 0 1 20 5.5v13a1.5 1.5 0 0 1-1.5 1.5H12V4Z" fill={color} opacity="0.75" />
          <path d="M8 8h2M8 11h2" stroke="#fff" strokeWidth="1.4" strokeLinecap="round" />
        </svg>
      );
    case 2: // search / gap
      return (
        <svg {...common}>
          <circle cx="10.5" cy="10.5" r="6" stroke={color} strokeWidth="2.2" fill={`${color}22`} />
          <path d="M15.5 15.5 20 20" stroke={color} strokeWidth="2.4" strokeLinecap="round" />
          <path d="M8 10.5h5" stroke={color} strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      );
    case 3: // puzzle
      return (
        <svg {...common}>
          <path
            d="M9 3.5a2 2 0 0 1 2 2V7h2.5a2 2 0 1 1 0 4H11v2.5a2 2 0 1 1-4 0V11H4.5a2 2 0 1 1 0-4H7V5.5a2 2 0 0 1 2-2Z"
            fill={color}
          />
          <path
            d="M15 11.5a2 2 0 0 1 2 2V15h1.5a2 2 0 1 1 0 4H17v1.5a2 2 0 1 1-4 0V19h-1.5a2 2 0 1 1 0-4H13v-1.5a2 2 0 0 1 2-2Z"
            fill={color}
            opacity="0.7"
          />
        </svg>
      );
    case 4: // gear
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="3.2" fill={color} />
          <path
            d="M12 3.2 13.2 6l2.9-.8 1.6 2.5 2.7 1.2-.7 2.9 2.1 2.1-2.1 2.1.7 2.9-2.7 1.2-1.6 2.5-2.9-.8L12 20.8l-1.2-2.8-2.9.8-1.6-2.5-2.7-1.2.7-2.9L2.2 12l2.1-2.1-.7-2.9 2.7-1.2L7.9 5.2l2.9.8L12 3.2Z"
            stroke={color}
            strokeWidth="1.6"
            fill={`${color}33`}
          />
        </svg>
      );
    case 5: // graph network
      return (
        <svg {...common}>
          <circle cx="6" cy="7" r="2.4" fill={color} />
          <circle cx="18" cy="6" r="2.4" fill={color} opacity="0.85" />
          <circle cx="12" cy="14" r="2.6" fill={color} />
          <circle cx="7" cy="19" r="2.2" fill={color} opacity="0.75" />
          <circle cx="18" cy="18" r="2.2" fill={color} opacity="0.75" />
          <path
            d="M8 8.2 10.5 12.5M16.2 7.5 13.5 12.2M12 16.5 8.8 17.8M14 15.8 16.5 17"
            stroke={color}
            strokeWidth="1.6"
          />
        </svg>
      );
    case 6: // bar chart
      return (
        <svg {...common}>
          <rect x="4" y="12" width="3.5" height="8" rx="1" fill={color} opacity="0.7" />
          <rect x="10" y="7" width="3.5" height="13" rx="1" fill={color} />
          <rect x="16" y="4" width="3.5" height="16" rx="1" fill={color} opacity="0.85" />
        </svg>
      );
    case 7: // database
      return (
        <svg {...common}>
          <ellipse cx="12" cy="6" rx="7" ry="2.8" fill={color} />
          <path d="M5 6v8c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8V6" stroke={color} strokeWidth="1.8" fill={`${color}22`} />
          <path d="M5 10c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8" stroke={color} strokeWidth="1.5" />
          <path d="M5 14c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8" stroke={color} strokeWidth="1.5" />
        </svg>
      );
    case 8: // monitor
      return (
        <svg {...common}>
          <rect x="3" y="4" width="18" height="12" rx="2" fill={color} />
          <rect x="5" y="6" width="14" height="8" rx="1" fill="#fff" opacity="0.9" />
          <path d="M9 19h6M12 16v3" stroke={color} strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      );
    case 9: // flask
      return (
        <svg {...common}>
          <path d="M9 3h6M10 3v5.2L5.5 18.5A2 2 0 0 0 7.3 21h9.4a2 2 0 0 0 1.8-2.5L14 8.2V3" stroke={color} strokeWidth="1.8" fill={`${color}28`} strokeLinejoin="round" />
          <path d="M7 15.5h10" stroke={color} strokeWidth="1.4" strokeLinecap="round" />
        </svg>
      );
    case 10: // trend up
      return (
        <svg {...common}>
          <path d="M4 16 10 10l4 4 6-8" stroke={color} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
          <path d="M14 6h6v6" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    case 11: // microscope / ablation
      return (
        <svg {...common}>
          <path d="M8 4v7M8 7h5" stroke={color} strokeWidth="2" strokeLinecap="round" />
          <circle cx="14.5" cy="12.5" r="3.2" stroke={color} strokeWidth="1.8" fill={`${color}30`} />
          <path d="M12.5 15.2 7 20.5M5 20.5h10" stroke={color} strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      );
    case 12: // complexity / function
      return (
        <svg {...common}>
          <rect x="3" y="3" width="18" height="18" rx="3" fill={`${color}22`} stroke={color} strokeWidth="1.6" />
          <path d="M8 16c1.2-4 2-6 4-6s2.8 2 4 6" stroke={color} strokeWidth="2" strokeLinecap="round" fill="none" />
          <path d="M7 8h3M14 8h3" stroke={color} strokeWidth="1.6" strokeLinecap="round" />
        </svg>
      );
    case 13: // document
      return (
        <svg {...common}>
          <path d="M7 3h7l4 4v14a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z" fill={color} />
          <path d="M14 3v4h4" fill="#fff" opacity="0.35" />
          <path d="M9 12h6M9 15h5" stroke="#fff" strokeWidth="1.5" strokeLinecap="round" />
        </svg>
      );
    case 14: // thesis book
      return (
        <svg {...common}>
          <path d="M5 4h11a2 2 0 0 1 2 2v13H7a2 2 0 0 0-2 2V4Z" fill={color} />
          <path d="M7 19a2 2 0 0 1 2-2h11v2a1 1 0 0 1-1 1H7Z" fill={color} opacity="0.7" />
          <path d="M9 8h6M9 11h5" stroke="#fff" strokeWidth="1.4" strokeLinecap="round" />
        </svg>
      );
    case 15: // graduation cap
      return (
        <svg {...common}>
          <path d="M2.5 10 12 5l9.5 5L12 15 2.5 10Z" fill={color} />
          <path d="M6 12v4.5c1.8 1.4 3.8 2.1 6 2.1s4.2-.7 6-2.1V12" stroke={color} strokeWidth="1.7" fill={`${color}33`} />
          <path d="M20 10.2V16" stroke={color} strokeWidth="1.7" strokeLinecap="round" />
        </svg>
      );
    case 16: // shield / practical SOC app
      return (
        <svg {...common}>
          <path
            d="M12 3 5 6v5.5c0 4.2 2.7 7.2 7 8.5 4.3-1.3 7-4.3 7-8.5V6L12 3Z"
            fill={`${color}28`}
            stroke={color}
            strokeWidth="1.7"
          />
          <path d="M9 12.2 11 14.2 15.2 10" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      );
    default:
      return (
        <svg {...common}>
          <circle cx="12" cy="12" r="8" fill={color} />
        </svg>
      );
  }
}

/** Task-level tinted bullet using parent step color. */
export function TaskIcon({
  stepId,
  index,
  size = 18,
}: {
  stepId: number;
  index: number;
  size?: number;
}) {
  const base = STEP_COLORS[stepId] ?? "#0D7377";
  const hues = [1, 0.82, 0.68, 0.9, 0.75];
  const opacity = hues[index % hues.length];
  return (
    <span
      className="task-icon"
      style={{
        width: size,
        height: size,
        background: base,
        opacity,
        boxShadow: `0 0 0 2px ${base}22`,
      }}
      aria-hidden
    >
      {index + 1}
    </span>
  );
}
