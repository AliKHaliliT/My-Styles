/** A berth as the rest of the application knows it. */
export interface Berth {
  readonly id: string
  readonly name: string
  /** Charted depth alongside, in meters. */
  readonly depthMeters: number
  /** Id of the vessel moored here; null when the berth is free. */
  readonly occupiedBy: string | null
}

/**
 * Filters a berth list down to the free ones.
 *
 * @param berths - The berths to filter.
 *
 * @returns The berths with no vessel alongside.
 */
export function freeBerths(berths: readonly Berth[]): Berth[] {
  return berths.filter((berth) => berth.occupiedBy === null)
}
