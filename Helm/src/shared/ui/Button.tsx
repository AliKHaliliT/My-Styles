import type { ButtonHTMLAttributes } from "react"

import { cn } from "@/shared/lib"

/** Visual weight of the action. */
export type ButtonVariant = "primary" | "ghost" | "danger"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Defaults to "primary". */
  variant?: ButtonVariant
}

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  primary: "bg-signal text-surface hover:opacity-90",
  ghost: "border border-line text-ink hover:bg-card",
  danger: "border border-alert text-alert hover:bg-alert hover:text-surface",
}

/**
 * The one button of the design system.
 *
 * Defaults to `type="button"` so a stray press inside a form never submits it
 * by accident; submit buttons opt in explicitly.
 */
export function Button({ variant = "primary", className, type, ...rest }: ButtonProps) {
  return (
    <button
      type={type ?? "button"}
      className={cn(
        "rounded-md px-4 py-2 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50",
        VARIANT_CLASSES[variant],
        className,
      )}
      {...rest}
    />
  )
}
