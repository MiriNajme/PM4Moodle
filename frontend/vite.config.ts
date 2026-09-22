import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";

// `npm run build` runs `tsc -b`, which type-checks this file against
// tsconfig.node.json — ES2023 lib only, no Node type definitions. Declaring the
// one global we need keeps @types/node out of the dependency list.
declare const process: { env: Record<string, string | undefined> };

// https://vite.dev/config/
export default defineConfig({
  // Where the built app will be served from. "/" for the local demo; the server
  // deployment builds with VITE_BASE_PATH=/pm4moodle/ so that asset URLs and
  // the router agree with the public path. See docker-compose.prod.yml.
  base: process.env.VITE_BASE_PATH || "/",
  plugins: [react(), tailwindcss()],
});
