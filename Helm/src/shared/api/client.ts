/**
 * The single HTTP door of the application.
 *
 * Nothing outside this module calls `fetch`. Every response body is parsed
 * against a zod schema before it is allowed past the boundary, so the rest of
 * the code handles typed data or a typed failure, never a raw payload.
 */
import type { ZodType } from "zod"

import { env } from "@/shared/config"

import { ApiError, WireContractError } from "./errors"

/** Supplies the current bearer token, or null when no session exists. */
export type TokenProvider = () => string | null

let tokenProvider: TokenProvider = () => null

/**
 * Registers the function the client asks for a bearer token on each request.
 *
 * The client lives in the shared layer and must not import the auth feature,
 * so the app layer injects the session lookup here at bootstrap. This is the
 * dependency rule pointed inward.
 *
 * @param provider - Called once per request; return null to send no token.
 *
 * @returns Nothing.
 */
export function setTokenProvider(provider: TokenProvider): void {
  tokenProvider = provider
}

/** Options accepted by {@link request}. */
export interface RequestOptions {
  /** HTTP method. Defaults to "GET". */
  method?: "GET" | "POST" | "PATCH" | "DELETE"
  /** JSON-serializable request body. */
  body?: unknown
}

/**
 * Fields a refusal's readable reason may sit in, in the order they are read.
 *
 * The family's server answers every refusal with `title`, `detail`,
 * `status_code`, and `type`, the reason living in `detail`; a plainer backend
 * answers with `message`; a validation refusal lists its reasons under
 * `detail` and keeps its readable text in `title`.
 */
const ERROR_MESSAGE_FIELDS = ["detail", "message", "title"] as const

/**
 * Extracts a human-readable message from an error response.
 *
 * @param response - The non-2xx response.
 *
 * @returns The first of the body's `detail`, `message`, and `title` fields
 *   that is a non-empty string, and the status text or code otherwise.
 */
async function readErrorMessage(response: Response): Promise<string> {
  try {
    const payload: unknown = await response.json()
    if (typeof payload === "object" && payload !== null) {
      for (const field of ERROR_MESSAGE_FIELDS) {
        const value: unknown = (payload as Record<string, unknown>)[field]
        if (typeof value === "string" && value !== "") {
          return value
        }
      }
    }
  } catch {
    // The body was not JSON; the status line is all there is.
  }
  return response.statusText === "" ? `Request failed with status ${String(response.status)}` : response.statusText
}

/**
 * Performs a request against the configured API and validates the response.
 *
 * @param path - Path appended to the configured base URL, starting with "/".
 * @param schema - Zod schema the response body must satisfy.
 * @param options - Method and body; defaults to a bare GET.
 *
 * @returns The validated response payload.
 *
 * @throws ApiError
 *   When the backend answers with a non-2xx status.
 * @throws WireContractError
 *   When the response body does not satisfy `schema`.
 */
export async function request<T>(path: string, schema: ZodType<T>, options: RequestOptions = {}): Promise<T> {
  const headers: Record<string, string> = { Accept: "application/json" }

  const token = tokenProvider()
  if (token !== null) {
    headers["Authorization"] = `Bearer ${token}`
  }

  let body: string | undefined
  if (options.body !== undefined) {
    headers["Content-Type"] = "application/json"
    body = JSON.stringify(options.body)
  }

  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    method: options.method ?? "GET",
    headers,
    body,
  })

  if (!response.ok) {
    throw new ApiError(response.status, await readErrorMessage(response))
  }

  const payload: unknown = await response.json()
  const parsed = schema.safeParse(payload)
  if (!parsed.success) {
    throw new WireContractError(path, parsed.error.message)
  }

  return parsed.data
}
