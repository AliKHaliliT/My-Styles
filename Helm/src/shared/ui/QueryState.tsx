import type { ReactNode } from "react"

import type { UseQueryResult } from "@tanstack/react-query"

import { ErrorState } from "./ErrorState"
import { Spinner } from "./Spinner"

interface QueryStateProps<TData> {
  /** The query whose lifecycle this component renders. */
  query: UseQueryResult<TData>
  /** Rendered instead of children when `isEmpty` judges the data empty. */
  empty?: ReactNode
  /** Decides emptiness of successful data. Defaults to "an empty array". */
  isEmpty?: (data: TData) => boolean
  /** Text for the pending spinner. */
  pendingLabel?: string | undefined
  /** Renders the successful, non-empty data. */
  children: (data: TData) => ReactNode
}

/**
 * Judges emptiness when the caller does not.
 *
 * @param data - The successful query data.
 *
 * @returns True only for an empty array.
 */
function defaultIsEmpty(data: unknown): boolean {
  return Array.isArray(data) && data.length === 0
}

/**
 * Renders the four states of a query in one place.
 *
 * Pending, error, empty, and success are first-class shapes here, so pages
 * never re-implement the ladder with ad hoc conditionals.
 *
 * @example
 * ```tsx
 * <QueryState query={useVessels()} empty={<EmptyState title="No vessels on the books." />}>
 *   {(vessels) => <VesselTable vessels={vessels} />}
 * </QueryState>
 * ```
 */
export function QueryState<TData>({
  query,
  empty,
  isEmpty = defaultIsEmpty,
  pendingLabel,
  children,
}: QueryStateProps<TData>): ReactNode {
  if (query.isPending) {
    return <Spinner label={pendingLabel} />
  }
  if (query.isError) {
    return (
      <ErrorState
        message={query.error.message}
        onRetry={() => {
          void query.refetch()
        }}
      />
    )
  }
  if (empty !== undefined && isEmpty(query.data)) {
    return empty
  }
  return children(query.data)
}
