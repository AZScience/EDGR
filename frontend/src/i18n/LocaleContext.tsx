import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  formatMessage,
  MESSAGES,
  type Lang,
  type MessageKey,
} from "./messages";

const STORAGE_KEY = "edgr.lang";

type LocaleCtx = {
  lang: Lang;
  setLang: (lang: Lang) => void;
  t: (key: MessageKey, vars?: Record<string, string | number>) => string;
  pick: <T>(vi: T, en: T) => T;
};

const Ctx = createContext<LocaleCtx | null>(null);

function readStoredLang(): Lang {
  try {
    const v = localStorage.getItem(STORAGE_KEY);
    if (v === "en" || v === "vi") return v;
  } catch {
    /* ignore */
  }
  return "vi";
}

export function LocaleProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>(() => readStoredLang());

  const setLang = useCallback((next: Lang) => {
    setLangState(next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  const t = useCallback(
    (key: MessageKey, vars?: Record<string, string | number>) =>
      formatMessage(MESSAGES[lang][key] ?? MESSAGES.vi[key] ?? key, vars),
    [lang],
  );

  const pick = useCallback(
    <T,>(viVal: T, enVal: T) => (lang === "en" ? enVal : viVal),
    [lang],
  );

  const value = useMemo(
    () => ({ lang, setLang, t, pick }),
    [lang, setLang, t, pick],
  );

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useLocale(): LocaleCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useLocale must be used within LocaleProvider");
  return ctx;
}
