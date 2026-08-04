import type { ReactNode } from "react"

interface EmptyStateProps {
  /** One line stating what is absent. */
  title: string
  /** Optional guidance or action, rendered under the title. */
  children?: ReactNode
}

/** The empty state of a list or collection, stated rather than implied. */
export function EmptyState({ title, children }: EmptyStateProps) {
  return (
    <div className="rounded-lg border border-dashed border-line p-8 text-center text-sm text-muted">
      <p className="font-medium text-ink">{title}</p>
      {children !== undefined ? <div className="mt-2">{children}</div> : null}
    </div>
  )
}
