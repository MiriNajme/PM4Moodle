import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "@radix-ui/themes/styles.css";
import { Theme } from "@radix-ui/themes";
import App from "./App";
import { BrowserRouter } from "react-router-dom";

// import.meta.env.BASE_URL is whatever `base` was set to at build time ("/" for
// the local demo, "/pm4moodle/" on the server). Passing it as the router's
// basename keeps /preview/image and /preview/json working under either.
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <Theme>
        <App />
      </Theme>
    </BrowserRouter>
  </StrictMode>
);
