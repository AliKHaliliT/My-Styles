import { z } from "zod"

export const berthDtoSchema = z.object({
  id: z.string(),
  name: z.string(),
  depth_m: z.number(),
  occupied_by: z.string().nullable(),
})

export const berthListDtoSchema = z.array(berthDtoSchema)

export type BerthDto = z.infer<typeof berthDtoSchema>
