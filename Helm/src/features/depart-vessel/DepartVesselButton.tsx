import { useQueryClient } from "@tanstack/react-query"

import { berthKeys } from "@/entities/berth"
import { useMarkDeparted } from "@/entities/vessel"
import { describeError } from "@/shared/api"
import { Button } from "@/shared/ui"

interface DepartVesselButtonProps {
  vesselId: string
}

/**
 * Records a moored vessel's departure.
 *
 * This interaction is a feature rather than a page-level button because it
 * spans two entities. The vessel slice invalidates its own caches, and this
 * feature adds the berth invalidation, since departing frees a berth.
 */
export function DepartVesselButton({ vesselId }: DepartVesselButtonProps) {
  const queryClient = useQueryClient()
  const mutation = useMarkDeparted()

  return (
    <div>
      <Button
        variant="danger"
        disabled={mutation.isPending}
        onClick={() => {
          mutation.mutate(vesselId, {
            onSuccess: async () => {
              await queryClient.invalidateQueries({ queryKey: berthKeys.all })
            },
          })
        }}
      >
        {mutation.isPending ? "Recording departure" : "Record departure"}
      </Button>
      {mutation.isError ? (
        <p role="alert" className="mt-2 text-sm text-alert">
          {describeError(mutation.error)}
        </p>
      ) : null}
    </div>
  )
}
