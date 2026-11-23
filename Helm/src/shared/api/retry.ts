/**
 * Which failed queries are asked again.
 *
 * A refusal and a broken contract are answers, and asking again brings the
 * same answer back, so neither is retried. A failure that carries no answer,
 * a lost connection or the server's own error, is asked again as the cache
 * would by default, three times with a growing wait between.
 */
import { ApiError, WireContractError } from "./errors"

/** How many times a failure that carries no answer is asked again, the cache's own default. */
const RETRIES = 3

/**
 * Decides whether a failed query is asked again.
 *
 * @param failureCount - How many times the query has failed before this decision, from zero.
 * @param error - What the last attempt threw.
 *
 * @returns True when the failure carried no answer and the retries are not yet spent.
 */
export function shouldRetry(failureCount: number, error: unknown): boolean {
  if (error instanceof WireContractError) return false
  if (error instanceof ApiError && error.status < 500) return false
  return failureCount < RETRIES
}
