import { StrictMode } from "react"

import { createRoot } from "react-dom/client"

import { env } from "@/shared/config"

import { App } from "./App"
import { initTheme } from "./layout/theme"
import { wireTokenProvider } from "./providers"

import "./styles/index.css"

/**
 * Boots the application.
 *
 * All wiring that must happen before first render lives here and nowhere
 * else: the token provider, the theme, and (in mock mode) the in-browser API
 * worker. Modules do no such work at import time.
 *
 * @returns Nothing, once the app is mounted.
 *
 * @throws Error
 *   When index.html carries no #root element to mount into.
 */
async function bootstrap(): Promise<void> {
  wireTokenProvider()
  initTheme()

  if (env.apiMode === "mock") {
    const { worker } = await import("@/mocks/browser")
    await worker.start({
      onUnhandledRequest: "bypass",
      serviceWorker: { url: `${env.baseUrl}mockServiceWorker.js` },
    })
  }

  const container = document.getElementById("root")
  if (container === null) {
    throw new Error("The #root element is missing from index.html")
  }

  createRoot(container).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}

void bootstrap()
