import { useNavigate } from "react-router-dom"

import { ScheduleArrivalForm } from "@/features/schedule-arrival"
import { Card, PageHeader } from "@/shared/ui"

/** Hosts the schedule-arrival form and walks to the new vessel on success. */
export function SchedulePage() {
  const navigate = useNavigate()

  return (
    <div className="mx-auto max-w-lg">
      <PageHeader title="Schedule an arrival" />
      <Card>
        <ScheduleArrivalForm
          onScheduled={(vessel) => {
            void navigate(`/vessels/${vessel.id}`)
          }}
        />
      </Card>
    </div>
  )
}
