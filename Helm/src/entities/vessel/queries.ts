/**
 * The vessel slice's server-cache bindings.
 *
 * Query keys are defined once here; anything that needs to invalidate vessel
 * data imports these keys instead of retyping strings.
 */
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import type { UseMutationResult, UseQueryResult } from "@tanstack/react-query"

import { fetchVessel, fetchVessels, markDeparted, scheduleArrival } from "./api"
import type { ArrivalInput, Vessel } from "./model"

/** Cache keys for everything vessel-shaped. */
export const vesselKeys = {
  all: ["vessels"] as const,
  detail: (id: string) => ["vessels", id] as const,
}

/**
 * Subscribes to the full vessel list.
 *
 * @returns The query for every vessel on the books.
 */
export function useVessels(): UseQueryResult<Vessel[]> {
  return useQuery({ queryKey: vesselKeys.all, queryFn: fetchVessels })
}

/**
 * Subscribes to one vessel.
 *
 * @param id - The vessel's identifier.
 *
 * @returns The query for that vessel.
 */
export function useVessel(id: string): UseQueryResult<Vessel> {
  return useQuery({ queryKey: vesselKeys.detail(id), queryFn: () => fetchVessel(id) })
}

/**
 * Provides the schedule-arrival mutation, invalidating the vessel list on
 * success.
 *
 * @returns The mutation.
 */
export function useScheduleArrival(): UseMutationResult<Vessel, Error, ArrivalInput> {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: scheduleArrival,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: vesselKeys.all })
    },
  })
}

/**
 * Provides the mark-departed mutation, invalidating this slice's own caches
 * on success. Effects on other slices are the caller's concern.
 *
 * @returns The mutation, taking the vessel id.
 */
export function useMarkDeparted(): UseMutationResult<Vessel, Error, string> {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: markDeparted,
    onSuccess: async (vessel) => {
      await queryClient.invalidateQueries({ queryKey: vesselKeys.all })
      await queryClient.invalidateQueries({ queryKey: vesselKeys.detail(vessel.id) })
    },
  })
}
