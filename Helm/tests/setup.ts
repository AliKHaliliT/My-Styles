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
  // No request leaves the loopback. A request no handler answers is refused here, so a call that
  // would reach a real host fails in the test instead, and a test that must reach one names it
  // in a handler, in the open.
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
