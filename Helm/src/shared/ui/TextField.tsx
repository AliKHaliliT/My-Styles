import type { InputHTMLAttributes, Ref } from "react"

import { cn } from "@/shared/lib"

interface TextFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  /** Visible label wrapping the input. */
  label: string
  /** Validation message; its presence switches the field into its error look. */
  error?: string | undefined
  /** Forwarded to the underlying input, so form libraries can register it. */
  ref?: Ref<HTMLInputElement>
}

/**
 * A labeled input with inline validation display.
 *
 * @example
 * ```tsx
 * <TextField label="Vessel name" error={errors.vesselName?.message} {...register("vesselName")} />
 * ```
 */
export function TextField({ label, error, className, ref, ...rest }: TextFieldProps) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block font-medium text-ink">{label}</span>
      <input
        ref={ref}
        className={cn(
          "w-full rounded-md border border-line bg-card px-3 py-2 text-ink outline-none focus:border-signal",
          error !== undefined && "border-alert",
          className,
        )}
        {...rest}
      />
      {error !== undefined ? (
        <span role="alert" className="mt-1 block text-alert">
          {error}
        </span>
      ) : null}
    </label>
  )
}
