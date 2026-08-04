import { Button } from "./Button"

interface ErrorStateProps {
  /** What went wrong, in words fit for the screen. */
  message: string
  /** Invoked by the retry button; omit to hide the button. */
  onRetry?: (() => void) | undefined
}

/** The failure state of anything asynchronous, with an optional retry. */
export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="rounded-lg border border-alert/40 bg-card p-5 text-sm" role="alert">
      <p className="font-medium text-alert">{message}</p>
      {onRetry !== undefined ? (
        <Button variant="ghost" className="mt-3" onClick={onRetry}>
          Try again
        </Button>
      ) : null}
    </div>
  )
}
