/**
 * Vessel endpoints, expressed in domain terms.
 *
 * Each function goes through the shared client, so every response is
 * schema-validated before the translator shapes it into the domain model.
 */
import { request } from "@/shared/api"

import { vesselDtoSchema, vesselListDtoSchema } from "./dto"
import type { ArrivalInput, Vessel } from "./model"
import { arrivalInputToDto, vesselFromDto } from "./translate"

/**
 * Fetches every vessel on the harbor's books.
 *
 * @returns The full vessel list.
 */
export async function fetchVessels(): Promise<Vessel[]> {
  const dtos = await request("/vessels", vesselListDtoSchema)
  return dtos.map(vesselFromDto)
}

/**
 * Fetches one vessel by id.
 *
 * @param id - The vessel's identifier.
 *
 * @returns The vessel.
 */
export async function fetchVessel(id: string): Promise<Vessel> {
  const dto = await request(`/vessels/${id}`, vesselDtoSchema)
  return vesselFromDto(dto)
}

/**
 * Puts a new arrival on the books.
 *
 * @param input - The arrival to schedule.
 *
 * @returns The created vessel, as the backend recorded it.
 */
export async function scheduleArrival(input: ArrivalInput): Promise<Vessel> {
  const dto = await request("/arrivals", vesselDtoSchema, {
    method: "POST",
    body: arrivalInputToDto(input),
  })
  return vesselFromDto(dto)
}

/**
 * Records a moored vessel's departure.
 *
 * @param id - The vessel's identifier.
 *
 * @returns The updated vessel.
 */
export async function markDeparted(id: string): Promise<Vessel> {
  const dto = await request(`/vessels/${id}/departure`, vesselDtoSchema, { method: "POST" })
  return vesselFromDto(dto)
}
