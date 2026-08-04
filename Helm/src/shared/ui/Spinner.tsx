interface SpinnerProps {
  /** Text shown beside the spinner. Defaults to "Fetching". */
  label?: string | undefined
}

/** The pending state of anything asynchronous. */
export function Spinner({ label }: SpinnerProps) {
  return (
    <div className="flex items-center gap-3 py-8 text-sm text-muted" role="status">
      <span className="size-5 animate-spin rounded-full border-2 border-line border-t-signal" aria-hidden="true" />
      <span>{label ?? "Fetching"}</span>
    </div>
  )
}
