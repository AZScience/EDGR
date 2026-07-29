import { useEffect, useId, useRef, useState } from "react";
import { useLocale } from "./LocaleContext";
import type { Lang } from "./messages";

const OPTIONS: { id: Lang; flag: string }[] = [
  { id: "vi", flag: "VN" },
  { id: "en", flag: "EN" },
];

export function LanguageMenu() {
  const { lang, setLang, t } = useLocale();
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const menuId = useId();

  useEffect(() => {
    if (!open) return;
    const onDoc = (e: MouseEvent) => {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("mousedown", onDoc);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDoc);
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  const current = OPTIONS.find((o) => o.id === lang) ?? OPTIONS[0];

  return (
    <div className="lang-menu" ref={rootRef}>
      <button
        type="button"
        className="lang-trigger"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={menuId}
        aria-label={t("lang_menu_aria")}
        onClick={() => setOpen((v) => !v)}
      >
        <span className="lang-flag">{current.flag}</span>
        <span className="lang-label">{t("lang_menu")}</span>
        <span className="lang-caret" aria-hidden>
          ▾
        </span>
      </button>
      {open ? (
        <ul
          id={menuId}
          className="lang-dropdown"
          role="listbox"
          aria-label={t("lang_menu")}
        >
          {OPTIONS.map((o) => (
            <li key={o.id} role="option" aria-selected={o.id === lang}>
              <button
                type="button"
                className={o.id === lang ? "active" : ""}
                onClick={() => {
                  setLang(o.id);
                  setOpen(false);
                }}
              >
                <span className="lang-flag">{o.flag}</span>
                <span>{o.id === "vi" ? t("lang_vi") : t("lang_en")}</span>
              </button>
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
