import { request } from "@/shared/api"

import { berthListDtoSchema } from "./dto"
import type { Berth } from "./model"
import { berthFromDto } from "./translate"

/**
 * Fetches every berth in the harbor.
 *
 * @returns The full berth list.
 */
export async function fetchBerths(): Promise<Berth[]> {
  const dtos = await request("/berths", berthListDtoSchema)
  return dtos.map(berthFromDto)
}
