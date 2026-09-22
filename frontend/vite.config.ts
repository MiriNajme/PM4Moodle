import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  // Where the built app will be served from. "/" for the local demo; the server
  // deployment builds with VITE_BASE_PATH=/pm4moodle/ so that asset URLs and
  // the router agree with the public path. See docker-compose.prod.yml.
  base: process.env.VITE_BASE_PATH || "/",
  plugins: [react(), tailwindcss()],
});
