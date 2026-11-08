import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5180,
    proxy: {
      "/api": {
        target: "http://localhost:8808",
        changeOrigin: true,
        auth: "demo:demo",
      },
    },
  },
});
