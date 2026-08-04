import { z } from "zod"

/**
 * What the schedule-arrival form validates before the domain sees anything.
 *
 * The ETA is kept as the raw `datetime-local` string here and converted to a
 * Date only when the values are translated into an `ArrivalInput`.
 */
export const scheduleArrivalSchema = z.object({
  vesselName: z.string().trim().min(2, "Name the vessel (at least 2 characters)."),
  flag: z.string().trim().min(2, "Name the flag state (at least 2 characters)."),
  eta: z.string().refine((value) => !Number.isNaN(Date.parse(value)), "Give a valid arrival time."),
  cargo: z.string().trim(),
})

export type ScheduleArrivalValues = z.infer<typeof scheduleArrivalSchema>
