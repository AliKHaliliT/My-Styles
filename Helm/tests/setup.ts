/**
 * Test lifecycle wiring.
 *
 * Every test runs against the same mock API the demo runs against, reset to
 * the pristine seed between cases, with the auth token provider cleared so
 * no test inherits another's session.
 */
import "@testing-library/jest-dom/vitest"

import { cleanup } from "@testing-library/react"
import { afterAll, afterEach, beforeAll } from "vitest"

import { resetDb } from "@/mocks/db"
import { server } from "@/mocks/node"
import { setTokenProvider } from "@/shared/api"

beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" })
})

afterEach(() => {
  cleanup()
  server.resetHandlers()
  resetDb()
  setTokenProvider(() => null)
  sessionStorage.clear()
  localStorage.clear()
})

afterAll(() => {
  server.close()
})
