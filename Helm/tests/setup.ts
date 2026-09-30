/**
 * Test lifecycle wiring.
 *
 * Every test runs against the same mock API the demo runs against, reset to
 * the pristine seed between cases, with the auth token provider cleared so
 * no test inherits another's session.
 */
import "@testing-library/jest-dom/vitest"

import { syncBuiltinESMExports } from "node:module"

import { cleanup } from "@testing-library/react"
import { afterAll, afterEach } from "vitest"

import { resetDb } from "@/mocks/db"
import { server } from "@/mocks/node"
import { setTokenProvider } from "@/shared/api"

// No request leaves the loopback. A request no handler answers is refused here, so a call that
// would reach a real host fails in the test instead, and a test that must reach one names it
// in a handler, in the open. The server starts as this file loads rather than in a hook, and
// Node's built-in module exports are synchronized right after, because a test file that imports
// the HTTP module's functions by name binds them as it loads, before any hook runs, and would
// otherwise hold the originals and reach a real host.
server.listen({ onUnhandledRequest: "error" })
syncBuiltinESMExports()

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
  syncBuiltinESMExports()
})
