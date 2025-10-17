import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import path from "path";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"), // points to src root
      "\\.module\\.css$": path.resolve(__dirname, "src/app/components/__mocks__/styleMock.ts"),
      "\\.css$": path.resolve(__dirname, "src/app/components/__mocks__/styleMock.ts"),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      exclude: [
    "vite.config.ts",
  "next.config.ts",
  "postcss.config.mjs",
  ".next/**",
  "node_modules/**",
  "coverage/**",
  "src/app/components/__mocks__/**",
  "src/app/components/__mocks__/**/*.ts",
  "src/app/types/graphql/**",
  "eslint.config.mjs",
  "next-env.d.ts",
  ],
    },
  },
});
