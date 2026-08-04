import { Link } from "react-router-dom"

import { freeBerths, useBerths } from "@/entities/berth"
import { countByStatus, isOverdue, useVessels } from "@/entities/vessel"
import { Card, PageHeader, QueryState } from "@/shared/ui"

interface StatCardProps {
  label: string
  value: number
  alert?: boolean
}

/** One number with its label; the dashboard is a row of these. */
function StatCard({ label, value, alert = false }: StatCardProps) {
  return (
    <Card>
      <p className={alert && value > 0 ? "text-3xl font-semibold text-alert" : "text-3xl font-semibold text-ink"}>
        {value}
      </p>
      <p className="mt-1 text-sm text-muted">{label}</p>
    </Card>
  )
}

/** The harbor at a glance: fleet counts, overdue arrivals, free berths. */
export function DashboardPage() {
  const vesselsQuery = useVessels()
  const berthsQuery = useBerths()

  return (
    <div>
      <PageHeader
        title="Harbor overview"
        action={
          <Link to="/schedule" className="text-sm font-medium text-signal hover:underline">
            Schedule an arrival
          </Link>
        }
      />
      <QueryState query={vesselsQuery} pendingLabel="Fetching the harbor's books">
        {(vessels) => {
          const counts = countByStatus(vessels)
          const now = new Date()
          const overdue = vessels.filter((vessel) => isOverdue(vessel, now)).length
          return (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <StatCard label="Due" value={counts.due} />
              <StatCard label="Moored" value={counts.moored} />
              <StatCard label="Departed" value={counts.departed} />
              <StatCard label="Overdue" value={overdue} alert />
            </div>
          )
        }}
      </QueryState>
      <div className="mt-4">
        <QueryState query={berthsQuery} pendingLabel="Fetching berth occupancy">
          {(berths) => (
            <Card>
              <p className="text-sm text-muted">
                <span className="font-medium text-ink">{freeBerths(berths).length}</span> of{" "}
                <span className="font-medium text-ink">{berths.length}</span> berths free
              </p>
            </Card>
          )}
        </QueryState>
      </div>
    </div>
  )
}
