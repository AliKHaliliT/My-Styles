/**
 * Typed access to the runtime environment.
 *
 * Every read of `import.meta.env` happens in this module. The rest of the
 * application imports the frozen `env` object and stays ignorant of where
 * configuration comes from, so swapping the source later touches one file.
 */

/** Which wire adapter the application talks to. */
export type ApiMode = "mock" | "live"

/** The validated runtime configuration. */
export interface Env {
  /** "mock" serves the in-browser demo API; "live" targets a real backend. */
  readonly apiMode: ApiMode
  /** Base URL prefixed to every API path. */
  readonly apiBaseUrl: string
  /** The path the app is served under; Vite's base, "/" in development. */
  readonly baseUrl: string
}

/**
 * Reads the API mode, defaulting anything unrecognized to "mock".
 *
 * @returns The resolved mode. Unknown values fall back to "mock" so a typo in
 *   an env file degrades to the offline demo instead of a broken deploy.
 */
function readApiMode(): ApiMode {
  return import.meta.env["VITE_API_MODE"] === "live" ? "live" : "mock"
}

/**
 * Reads the API base URL, defaulting to the same-origin "/api" prefix.
 *
 * @returns The base URL with no trailing slash trimmed or added.
 */
function readApiBaseUrl(): string {
  const raw: unknown = import.meta.env["VITE_API_BASE_URL"]
  return typeof raw === "string" && raw !== "" ? raw : "/api"
}

export const env: Env = Object.freeze({
  apiMode: readApiMode(),
  apiBaseUrl: readApiBaseUrl(),
  baseUrl: import.meta.env.BASE_URL,
})
