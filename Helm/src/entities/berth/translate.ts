import type { BerthDto } from "./dto"
import type { Berth } from "./model"

/**
 * Convert a wire berth into the domain model.
 */
export function berthFromDto(dto: BerthDto): Berth {
  return {
    id: dto.id,
    name: dto.name,
    depthMeters: dto.depth_m,
    occupiedBy: dto.occupied_by,
  }
}
