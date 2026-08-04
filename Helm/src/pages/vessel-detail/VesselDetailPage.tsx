import type { ReactNode } from "react"

import { useParams } from "react-router-dom"

import { useBerths } from "@/entities/berth"
import { VesselStatusBadge, useVessel } from "@/entities/vessel"
import { DepartVesselButton } from "@/features/depart-vessel"
import { formatDateTime } from "@/shared/lib"
import { Card, ErrorState, PageHeader, QueryState } from "@/shared/ui"

interface RowProps {
  label: string
  children: ReactNode
}

/** One labeled line of the dossier. */
function Row({ label, children }: RowProps) {
  return (
    <div className="flex justify-between gap-4 border-b border-line py-2 text-sm last:border-b-0">
      <dt className="text-muted">{label}</dt>
      <dd className="text-right text-ink">{children}</dd>
    </div>
  )
}

/** One vessel's full record, with the departure action when it applies. */
export function VesselDetailPage() {
  const params = useParams<{ id: string }>()
  const vesselId = params.id ?? ""
  const query = useVessel(vesselId)
  const berthsQuery = useBerths()

  if (vesselId === "") {
    return <ErrorState message="No vessel id in the address." />
  }

  return (
    <QueryState query={query} pendingLabel="Fetching the vessel's record">
      {(vessel) => {
        const berthName =
          vessel.berthId === null
            ? null
            : (berthsQuery.data?.find((berth) => berth.id === vessel.berthId)?.name ?? vessel.berthId)
        return (
          <div>
            <PageHeader title={vessel.name} action={<VesselStatusBadge vessel={vessel} />} />
            <Card>
              <dl>
                <Row label="Flag state">{vessel.flag}</Row>
                <Row label="Cargo">{vessel.cargo ?? "In ballast"}</Row>
                <Row label="ETA">{vessel.eta !== null ? formatDateTime(vessel.eta) : "Not expected"}</Row>
                <Row label="Berth">{berthName ?? "Not assigned"}</Row>
              </dl>
            </Card>
            {vessel.status === "moored" ? (
              <div className="mt-4">
                <DepartVesselButton vesselId={vessel.id} />
              </div>
            ) : null}
          </div>
        )
      }}
    </QueryState>
  )
}
