import { defineConfig } from "vite";

export default defineConfig({
  base: "/static",
  build: {
    manifest: "manifest.json",
    outDir: "./build",
    rollupOptions: {
      input: {
        "map.ts": "./src/map.ts",
        "elements.ts": "./src/elements.ts",
      },
    },
  },
});
