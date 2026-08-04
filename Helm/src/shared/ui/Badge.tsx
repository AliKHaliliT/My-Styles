import type { ReactNode } from "react"

import { cn } from "@/shared/lib"

/** Semantic tone of the badge; tones map to tokens, never to raw colors. */
export type BadgeTone = "neutral" | "ok" | "warn" | "alert"

interface BadgeProps {
  tone?: BadgeTone
  children: ReactNode
}

const TONE_CLASSES: Record<BadgeTone, string> = {
  neutral: "border-line text-muted",
  ok: "border-ok text-ok",
  warn: "border-warn text-warn",
  alert: "border-alert text-alert",
}

/** A small inline status marker. */
export function Badge({ tone = "neutral", children }: BadgeProps) {
  return (
    <span className={cn("inline-block rounded-full border px-2.5 py-0.5 text-xs font-medium", TONE_CLASSES[tone])}>
      {children}
    </span>
  )
}
