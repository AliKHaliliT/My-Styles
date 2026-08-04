/**
 * The vessel domain model and its pure logic.
 *
 * Everything here is plain data and plain functions. No fetching, no React,
 * no wire shapes; those live in the segments beside this one.
 */

/** Where a vessel stands in its harbor call. */
export type VesselStatus = "due" | "moored" | "departed"

/** A vessel as the rest of the application knows it. */
export interface Vessel {
  readonly id: string
  readonly name: string
  /** Flag state the vessel sails under. */
  readonly flag: string
  readonly status: VesselStatus
  /** Estimated arrival; null once the vessel is alongside or gone. */
  readonly eta: Date | null
  /** Berth the vessel is moored at; null unless status is "moored". */
  readonly berthId: string | null
  /** Declared cargo; null for a call in ballast. */
  readonly cargo: string | null
}

/** A request to put a new arrival on the books. */
export interface ArrivalInput {
  readonly vesselName: string
  readonly flag: string
  readonly eta: Date
  readonly cargo: string | null
}

/** Display labels for each status, so pages never switch on raw values. */
export const STATUS_LABELS: Record<VesselStatus, string> = {
  due: "Due",
  moored: "Moored",
  departed: "Departed",
}

/**
 * Decides whether a due vessel has blown past its ETA.
 *
 * @param vessel - The vessel to judge.
 * @param now - The moment to judge against, passed in so the logic stays pure.
 *
 * @returns True when the vessel is still due and its ETA lies in the past.
 */
export function isOverdue(vessel: Vessel, now: Date): boolean {
  return vessel.status === "due" && vessel.eta !== null && vessel.eta.getTime() < now.getTime()
}

/**
 * Counts vessels per status.
 *
 * @param vessels - The fleet to tally.
 *
 * @returns One count per status, with absent statuses counted as zero.
 */
export function countByStatus(vessels: readonly Vessel[]): Record<VesselStatus, number> {
  const counts: Record<VesselStatus, number> = { due: 0, moored: 0, departed: 0 }
  for (const vessel of vessels) {
    counts[vessel.status] += 1
  }
  return counts
}
