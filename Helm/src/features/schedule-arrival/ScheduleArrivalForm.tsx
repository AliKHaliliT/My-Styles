import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import type { Vessel } from "@/entities/vessel"
import { useScheduleArrival } from "@/entities/vessel"
import { describeError } from "@/shared/api"
import { Button, TextField } from "@/shared/ui"

import type { ScheduleArrivalValues } from "./schema"
import { scheduleArrivalSchema } from "./schema"

interface ScheduleArrivalFormProps {
  /** Called with the created vessel; the page decides where to go next. */
  onScheduled: (vessel: Vessel) => void
}

/**
 * The form that puts a new arrival on the books.
 *
 * Client-side validation guards the obvious mistakes; the mutation's own
 * error surfaces under the form when the harbor office rejects the request.
 */
export function ScheduleArrivalForm({ onScheduled }: ScheduleArrivalFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ScheduleArrivalValues>({
    resolver: zodResolver(scheduleArrivalSchema),
    defaultValues: { vesselName: "", flag: "", eta: "", cargo: "" },
  })

  const mutation = useScheduleArrival()

  const submit = handleSubmit((values) => {
    mutation.mutate(
      {
        vesselName: values.vesselName,
        flag: values.flag,
        eta: new Date(values.eta),
        cargo: values.cargo === "" ? null : values.cargo,
      },
      { onSuccess: onScheduled },
    )
  })

  return (
    <form
      className="space-y-4"
      onSubmit={(event) => {
        void submit(event)
      }}
    >
      <TextField label="Vessel name" error={errors.vesselName?.message} {...register("vesselName")} />
      <TextField label="Flag state" error={errors.flag?.message} {...register("flag")} />
      <TextField label="Estimated arrival" type="datetime-local" error={errors.eta?.message} {...register("eta")} />
      <TextField label="Cargo (leave empty for ballast)" error={errors.cargo?.message} {...register("cargo")} />
      {mutation.isError ? (
        <p role="alert" className="text-sm text-alert">
          {describeError(mutation.error)}
        </p>
      ) : null}
      <Button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Scheduling" : "Schedule arrival"}
      </Button>
    </form>
  )
}
