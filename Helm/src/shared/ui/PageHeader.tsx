import type { ReactNode } from "react"

interface PageHeaderProps {
  title: string
  /** Optional action area, rendered on the right edge. */
  action?: ReactNode
}

/** The standard page heading row. */
export function PageHeader({ title, action }: PageHeaderProps) {
  return (
    <div className="mb-6 flex items-center justify-between gap-4">
      <h1 className="text-2xl font-semibold text-ink">{title}</h1>
      {action !== undefined ? <div>{action}</div> : null}
    </div>
  )
}
