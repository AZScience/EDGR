import katex from "katex";
import type { ReactNode } from "react";
import "katex/dist/katex.min.css";

/** True when the string is already mostly TeX (skip aggressive ascii rewrites). */
function isMostlyLatex(s: string): boolean {
  return /\\[a-zA-Z]+/.test(s);
}

/** Wrap bare operator names, but never inside \mathrm{…} or after a backslash. */
function wrapOps(s: string, names: string[]): string {
  let out = s;
  for (const name of names) {
    const re = new RegExp(`(?<!\\\\)(?<!\\\\mathrm\\{)\\b${name}\\b`, "g");
    out = out.replace(re, `\\mathrm{${name}}`);
  }
  return out;
}

/** Convert common ascii/unicode formulas to KaTeX-ready latex. */
export function toLatex(expr: string): string {
  let s = expr.trim();
  if (!s) return s;

  // Strip common wrappers
  if (s.startsWith("$$") && s.endsWith("$$")) s = s.slice(2, -2).trim();
  else if (s.startsWith("$") && s.endsWith("$") && s.length > 2) {
    s = s.slice(1, -1).trim();
  }
  if (s.startsWith("\\(") && s.endsWith("\\)")) s = s.slice(2, -2).trim();
  if (s.startsWith("\\[") && s.endsWith("\\]")) s = s.slice(2, -2).trim();

  // Collapse over-escaped TeX commands: \\tau → \tau
  s = s.replace(/\\\\([a-zA-Z]+)/g, "\\$1");

  // Unicode → TeX (always)
  s = s
    .replace(/τ/g, "\\tau ")
    .replace(/ρ/g, "\\rho ")
    .replace(/θ/g, "\\theta ")
    .replace(/Φ/g, "\\Phi ")
    .replace(/φ/g, "\\varphi ")
    .replace(/∈/g, "\\in ")
    .replace(/⊆/g, "\\subseteq ")
    .replace(/∪/g, "\\cup ")
    .replace(/∩/g, "\\cap ")
    .replace(/∀/g, "\\forall ")
    .replace(/∧/g, "\\land ")
    .replace(/∝/g, "\\propto ")
    .replace(/↦/g, "\\mapsto ")
    .replace(/→/g, "\\rightarrow ")
    .replace(/↔/g, "\\leftrightarrow ")
    .replace(/≤/g, "\\le ")
    .replace(/≥/g, "\\ge ")
    .replace(/≈/g, "\\approx ")
    .replace(/≠/g, "\\neq ")
    .replace(/·/g, "\\cdot ")
    .replace(/×/g, "\\times ")
    .replace(/∑/g, "\\sum ")
    .replace(/Δ/g, "\\Delta ")
    .replace(/⊕/g, "\\oplus ")
    .replace(/∅/g, "\\emptyset ")
    .replace(/ℕ/g, "\\mathbb{N}")
    .replace(/ℝ/g, "\\mathbb{R}")
    .replace(/ℤ/g, "\\mathbb{Z}")
    .replace(/−/g, "-")
    .replace(/′/g, "'")
    .replace(/…/g, "\\ldots ")
    .replace(/\|([^|]+)\|/g, (_m, inner: string) => {
      // |P| → \lvert P\rvert when not already TeX delimiters
      if (String(inner).includes("\\")) return `|${inner}|`;
      return `\\lvert ${inner}\\rvert`;
    });

  // Ascii operator helpers — skip if already TeX-heavy (backend packs)
  if (!isMostlyLatex(s)) {
    s = wrapOps(s, [
      "TopK",
      "sim",
      "Extract",
      "Expand",
      "TemporalFilter",
      "Retrieve",
      "HallucinationRisk",
      "GapScore",
      "Pair",
      "LLM",
    ]);

    // O(E log V) → O(E\log V)
    s = s.replace(/\bO\(([^)]+)\)/g, (_m, inner: string) => {
      const fixed = String(inner).replace(/\blog\b/g, "\\log ");
      return `O(${fixed})`;
    });

    // Subscripts / starred symbols (skip if already _{...} / ^{...})
    if (!s.includes("_{") && !s.includes("^{")) {
      s = s.replace(/\b([A-Za-z]+)_([A-Za-z0-9*'+]+)\b/g, "$1_{$2}");
      s = s.replace(/\b([A-Za-z])\*/g, "$1^{*}");
    }

    // Simple fractions a/(b)
    s = s.replace(
      /\b([A-Za-z0-9\\_{}]+)\s*\/\s*\(([^)]+)\)/g,
      "\\frac{$1}{$2}",
    );
  } else {
    // Still wrap bare Pair/GapScore if they appear outside \mathrm
    s = wrapOps(s, ["GapScore", "Pair", "TopK", "HallucinationRisk"]);
  }

  return s;
}

/** Vietnamese / Latin prose — never feed to KaTeX (freezes the tab). */
function hasProseScript(s: string): boolean {
  return /[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/i.test(
    s,
  );
}

export function looksLikeFormula(s: string): boolean {
  const t = s.trim();
  if (!t || t.length > 220) return false;
  if (hasProseScript(t)) return false;
  return /[=\\_{}^]|\\in|O\(|\\le|\\ge|\\sum|\\frac|\\approx|τ|ρ|θ|Φ|φ|∈|⊆|≤|≥|≈|→|∝|≠|ℕ|ℝ|\|[^|]+\|/.test(
    t,
  );
}

function looksLikeSentence(s: string): boolean {
  const words = s.trim().split(/\s+/);
  if (words.length >= 8) return true;
  if (hasProseScript(s) && words.length >= 4) return true;
  if (/[a-z]{4,}/i.test(s) && words.length >= 8) return true;
  return /[.!?。]\s/.test(s);
}

function isSafeMathIsland(expr: string): boolean {
  const t = expr.trim();
  if (!t || t.length > 180) return false;
  if (hasProseScript(t)) return false;
  const words = t.split(/\s+/);
  if (words.length >= 6 && !/[=\\_{}^τρθ]/.test(t)) return false;
  return true;
}

/** Tokenize prose into text + math islands. */
export function splitMathProse(
  text: string,
): Array<{ type: "text" | "math"; value: string }> {
  const s = text ?? "";
  if (!s) return [];

  // Prose-heavy: only honor explicit math delimiters (never regex-scan `=`).
  // Bare scanning fed whole Vietnamese sentences into KaTeX → page hang.
  const delimitedOnly = hasProseScript(s) || s.length > 160;
  const re = delimitedOnly
    ? /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$|\\\(([\s\S]+?)\\\)|\\\[([\s\S]+?)\\\]/g
    : /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$|\\\(([\s\S]+?)\\\)|\\\[([\s\S]+?)\\\]|((?:[A-Za-z\\τρθΦφ][A-Za-z0-9_\\{}()^*'′]*)\s*[=≈≤≥∈]\s*[^.;,—]+|(?:[HFτρ])\s*[≈=]\s*[^\s.;,—]+|O\([^)]+\)|[τρθΦφ]\([^)]*\)(?:\s*[=≈]\s*[^.;,—]+)?)/g;

  const out: Array<{ type: "text" | "math"; value: string }> = [];
  let last = 0;
  let m: RegExpExecArray | null;
  let mathCount = 0;
  while ((m = re.exec(s)) !== null) {
    if (m.index > last) {
      out.push({ type: "text", value: s.slice(last, m.index) });
    }
    const math = (m[1] ?? m[2] ?? m[3] ?? m[4] ?? m[5] ?? m[0]).trim();
    if (isSafeMathIsland(math) && mathCount < 24) {
      out.push({ type: "math", value: math });
      mathCount += 1;
    } else {
      out.push({ type: "text", value: m[0] });
    }
    last = m.index + m[0].length;
  }
  if (last < s.length) out.push({ type: "text", value: s.slice(last) });
  return out.length ? out : [{ type: "text", value: s }];
}

function renderKatex(expr: string, display: boolean): string {
  try {
    const html = katex.renderToString(toLatex(expr), {
      throwOnError: false,
      displayMode: display,
      strict: "ignore",
      trust: false,
      output: "html",
    });
    if (!html || html.includes("katex-error")) return "";
    return html;
  } catch {
    return "";
  }
}

export function Formula({
  expr,
  display = true,
}: {
  expr: string;
  display?: boolean;
}) {
  const html = renderKatex(expr, display);
  if (!html) {
    return (
      <div className={`formula-fallback ${display ? "display" : "inline"}`}>
        {expr}
      </div>
    );
  }
  return (
    <div
      className={`formula-box ${display ? "display" : "inline"}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

/** Render prose with embedded KaTeX for formula-like spans. */
export function MathText({
  text,
  as: Tag = "span",
  className,
}: {
  text: string;
  as?: "span" | "p" | "div" | "li";
  className?: string;
}) {
  const raw = text ?? "";
  if (!raw) return null;

  // Fast path: Vietnamese / long prose without $ delimiters → plain text (no KaTeX).
  if (
    (hasProseScript(raw) || raw.length > 200) &&
    !/\$|\\\(|\\\[/.test(raw)
  ) {
    return <Tag className={className}>{raw}</Tag>;
  }

  if (looksLikeFormula(raw) && !looksLikeSentence(raw)) {
    if (Tag === "li" || Tag === "p" || Tag === "div") {
      return (
        <Tag className={className}>
          <Formula expr={raw} display />
        </Tag>
      );
    }
    return <Formula expr={raw} display />;
  }

  const parts = splitMathProse(raw);
  const hasMath = parts.some((p) => p.type === "math");
  if (!hasMath) {
    return <Tag className={className}>{raw}</Tag>;
  }

  const nodes: ReactNode[] = parts.map((p, i) => {
    if (p.type === "text") return <span key={i}>{p.value}</span>;
    const html = renderKatex(p.value, false);
    if (!html) {
      return (
        <code key={i} className="formula-inline-fallback">
          {p.value}
        </code>
      );
    }
    return (
      <span
        key={i}
        className="formula-inline"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    );
  });

  return <Tag className={className}>{nodes}</Tag>;
}
