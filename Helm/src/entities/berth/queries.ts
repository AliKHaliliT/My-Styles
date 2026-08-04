import { useQuery } from "@tanstack/react-query"
import type { UseQueryResult } from "@tanstack/react-query"

import { fetchBerths } from "./api"
import type { Berth } from "./model"

/** Cache keys for everything berth-shaped. */
export const berthKeys = {
  all: ["berths"] as const,
}

/**
 * Subscribes to the full berth list.
 *
 * @returns The query for every berth in the harbor.
 */
export function useBerths(): UseQueryResult<Berth[]> {
  return useQuery({ queryKey: berthKeys.all, queryFn: fetchBerths })
}
