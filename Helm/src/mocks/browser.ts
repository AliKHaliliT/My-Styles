import { setupWorker } from "msw/browser"

import { handlers } from "./handlers"

/** The in-browser demo API; started by the app bootstrap in mock mode. */
export const worker = setupWorker(...handlers)
