import { setupServer } from "msw/node"

import { handlers } from "./handlers"

/** The same demo API for Node, wired into the test lifecycle in tests/setup.ts. */
export const server = setupServer(...handlers)
