import type { ArrivalRequestDto, VesselDto } from "./dto"
import type { ArrivalInput, Vessel } from "./model"

/**
 * Convert a wire vessel into the domain model.
 */
export function vesselFromDto(dto: VesselDto): Vessel {
  return {
    id: dto.id,
    name: dto.name,
    flag: dto.flag,
    status: dto.status,
    eta: dto.eta === null ? null : new Date(dto.eta),
    berthId: dto.berth_id,
    cargo: dto.cargo,
  }
}

/**
 * Convert a domain arrival request into its outbound wire shape.
 */
export function arrivalInputToDto(input: ArrivalInput): ArrivalRequestDto {
  return {
    vessel_name: input.vesselName,
    flag: input.flag,
    eta: input.eta.toISOString(),
    cargo: input.cargo,
  }
}
