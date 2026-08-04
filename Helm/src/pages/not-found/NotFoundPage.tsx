import { Link } from "react-router-dom"

import { EmptyState } from "@/shared/ui"

/** The catch-all route. */
export function NotFoundPage() {
  return (
    <div className="py-16">
      <EmptyState title="Nothing is charted at this address.">
        <Link to="/" className="font-medium text-signal hover:underline">
          Back to the harbor overview
        </Link>
      </EmptyState>
    </div>
  )
}
