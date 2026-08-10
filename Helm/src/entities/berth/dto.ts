import { z } from "zod"

/** Wire shape of one berth as the backend sends it. */
export const berthDtoSchema = z.object({
  id: z.string(),
  name: z.string(),
  depth_m: z.number(),
  occupied_by: z.string().nullable(),
})

/** Wire shape of the berth collection. */
export const berthListDtoSchema = z.array(berthDtoSchema)

/** One berth exactly as it crosses the wire. */
export type BerthDto = z.infer<typeof berthDtoSchema>
