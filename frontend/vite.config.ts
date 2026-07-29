import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  // Production build served by FastAPI at /ui/ (Streamlit iframes that URL).
  // Dev server keeps root `/` so http://127.0.0.1:5180 still works.
  base: mode === "production" ? "/ui/" : "/",
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
}));
