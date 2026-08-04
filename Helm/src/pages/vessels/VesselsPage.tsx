import { useState } from "react"

import { Link } from "react-router-dom"

import type { VesselStatus } from "@/entities/vessel"
import { STATUS_LABELS, VesselStatusBadge, useVessels } from "@/entities/vessel"
import { formatDateTime } from "@/shared/lib"
import { EmptyState, PageHeader, QueryState } from "@/shared/ui"

type StatusFilter = VesselStatus | "all"

const FILTER_OPTIONS: readonly StatusFilter[] = ["all", "due", "moored", "departed"]

/**
 * The vessel ledger with filter and search.
 *
 * The filter and the search box are ephemeral UI state, so they live in
 * component state; only the vessel list itself comes from the server cache.
 */
export function VesselsPage() {
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all")
  const [search, setSearch] = useState("")
  const query = useVessels()

  return (
    <div>
      <PageHeader
        title="Vessels"
        action={
          <Link to="/schedule" className="text-sm font-medium text-signal hover:underline">
            Schedule an arrival
          </Link>
        }
      />
      <div className="mb-4 flex flex-wrap gap-3">
        <select
          aria-label="Filter by status"
          className="rounded-md border border-line bg-card px-3 py-2 text-sm text-ink"
          value={statusFilter}
          onChange={(event) => {
            setStatusFilter(event.target.value as StatusFilter)
          }}
        >
          {FILTER_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option === "all" ? "All statuses" : STATUS_LABELS[option]}
            </option>
          ))}
        </select>
        <input
          aria-label="Search by name"
          placeholder="Search by name"
          className="rounded-md border border-line bg-card px-3 py-2 text-sm text-ink outline-none focus:border-signal"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value)
          }}
        />
      </div>
      <QueryState
        query={query}
        pendingLabel="Fetching the vessel ledger"
        empty={<EmptyState title="No vessels on the books.">Schedule an arrival to open the ledger.</EmptyState>}
      >
        {(vessels) => {
          const needle = search.trim().toLowerCase()
          const visible = vessels.filter(
            (vessel) =>
              (statusFilter === "all" || vessel.status === statusFilter) &&
              (needle === "" || vessel.name.toLowerCase().includes(needle)),
          )
          if (visible.length === 0) {
            return <EmptyState title="Nothing matches the filter." />
          }
          return (
            <ul className="space-y-2">
              {visible.map((vessel) => (
                <li key={vessel.id}>
                  <Link
                    to={`/vessels/${vessel.id}`}
                    className="flex items-center justify-between gap-4 rounded-lg border border-line bg-card px-4 py-3 hover:border-signal"
                  >
                    <span>
                      <span className="block font-medium text-ink">{vessel.name}</span>
                      <span className="block text-sm text-muted">
                        {vessel.flag}
                        {vessel.eta !== null ? ` · ETA ${formatDateTime(vessel.eta)}` : ""}
                      </span>
                    </span>
                    <VesselStatusBadge vessel={vessel} />
                  </Link>
                </li>
              ))}
            </ul>
          )
        }}
      </QueryState>
    </div>
  )
}
