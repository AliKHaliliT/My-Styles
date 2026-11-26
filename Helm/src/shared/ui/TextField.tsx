import { useId, type InputHTMLAttributes, type Ref } from "react"

import { cn } from "@/shared/lib"

interface TextFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  /** Visible label, tied to the input by the input's id. */
  label: string
  /** Validation message; its presence switches the field into its error look. */
  error?: string | undefined
  /** Forwarded to the underlying input, so form libraries can register it. */
  ref?: Ref<HTMLInputElement>
}

/**
 * A labeled input with inline validation display.
 *
 * The message sits outside the label, so the input's accessible name stays the label while the
 * message shows, and the input carries the message as its description and is marked invalid.
 *
 * @example
 * ```tsx
 * <TextField label="Vessel name" error={errors.vesselName?.message} {...register("vesselName")} />
 * ```
 */
export function TextField({ label, error, className, ref, id, ...rest }: TextFieldProps) {
  const generatedId = useId()
  const inputId = id ?? generatedId
  const errorId = `${inputId}-error`
  return (
    <div className="block text-sm">
      <label htmlFor={inputId} className="mb-1 block font-medium text-ink">
        {label}
      </label>
      <input
        ref={ref}
        id={inputId}
        aria-invalid={error !== undefined ? true : undefined}
        aria-describedby={error !== undefined ? errorId : undefined}
        className={cn(
          "w-full rounded-md border border-edge bg-card px-3 py-2 text-ink outline-none focus:border-signal",
          error !== undefined && "border-alert",
          className,
        )}
        {...rest}
      />
      {error !== undefined ? (
        <span id={errorId} role="alert" className="mt-1 block text-alert">
          {error}
        </span>
      ) : null}
    </div>
  )
}
