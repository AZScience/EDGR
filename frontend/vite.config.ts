import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Vercel sets VERCEL=1. FastAPI serves SPA at /ui/; Vercel serves at /.
  const onVercel = Boolean(process.env.VERCEL);
  const baseEnv = process.env.VITE_BASE;
  const base =
    baseEnv !== undefined && baseEnv !== ""
      ? baseEnv
      : onVercel
        ? "/"
        : mode === "production"
          ? "/ui/"
          : "/";

  return {
    base,
    plugins: [react()],
    server: {
      host: "127.0.0.1",
      port: 5180,
      proxy: {
        "/api": {
          target: "http://127.0.0.1:8016",
          changeOrigin: true,
        },
      },
    },
  };
});
