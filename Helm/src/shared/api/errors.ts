/**
 * The two failure shapes of the wire boundary.
 *
 * An `ApiError` means the backend answered and said no. A
 * `WireContractError` means the backend answered with a payload that does not
 * match the schema this client was built against, which is a deploy-time
 * mismatch rather than a user-facing condition.
 */

/** The backend responded with a non-2xx status. */
export class ApiError extends Error {
  /** HTTP status code carried by the response. */
  readonly status: number

  /**
   * @param status - HTTP status code carried by the response.
   * @param message - Human-readable message, taken from the response body
   *   when the backend provides one.
   */
  constructor(status: number, message: string) {
    super(message)
    this.name = "ApiError"
    this.status = status
  }
}

/** The response body failed validation against the expected wire schema. */
export class WireContractError extends Error {
  /** The request path whose response broke the contract. */
  readonly path: string

  /**
   * @param path - The request path whose response broke the contract.
   * @param detail - The validation failure, as reported by the schema.
   */
  constructor(path: string, detail: string) {
    super(`The response from ${path} broke the wire contract. ${detail}`)
    this.name = "WireContractError"
    this.path = path
  }
}

/**
 * Turns any thrown value into a message fit for the UI.
 *
 * @param error - Whatever was thrown.
 *
 * @returns The error's own message when there is one, and a generic
 *   harbor-office apology otherwise.
 */
export function describeError(error: unknown): string {
  if (error instanceof Error && error.message !== "") {
    return error.message
  }
  return "Something went wrong while talking to the harbor office."
}
