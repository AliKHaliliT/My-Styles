/**
 * The vessel wire contract.
 *
 * These schemas describe what the backend actually sends, snake_case and
 * ISO strings included. They are parsed at the boundary and never leak past
 * the translators.
 */
import { z } from "zod"

export const vesselDtoSchema = z.object({
  id: z.string(),
  name: z.string(),
  flag: z.string(),
  status: z.enum(["due", "moored", "departed"]),
  eta: z.string().nullable(),
  berth_id: z.string().nullable(),
  cargo: z.string().nullable(),
})

export const vesselListDtoSchema = z.array(vesselDtoSchema)

export type VesselDto = z.infer<typeof vesselDtoSchema>

/** Outbound body for scheduling an arrival; built by the translator. */
export interface ArrivalRequestDto {
  vessel_name: string
  flag: string
  eta: string
  cargo: string | null
}
