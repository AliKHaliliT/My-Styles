import type { BadgeTone } from "@/shared/ui"
import { Badge } from "@/shared/ui"

import type { Vessel } from "./model"
import { STATUS_LABELS, isOverdue } from "./model"

const STATUS_TONES: Record<Vessel["status"], BadgeTone> = {
  due: "warn",
  moored: "ok",
  departed: "neutral",
}

interface VesselStatusBadgeProps {
  vessel: Vessel
  /** The moment to judge overdueness against. Defaults to now. */
  now?: Date
}

/**
 * The standard status marker for a vessel, with the overdue escalation.
 *
 * Every page shows vessel status through this component, so "what does
 * overdue look like" is decided exactly once.
 */
export function VesselStatusBadge({ vessel, now }: VesselStatusBadgeProps) {
  if (isOverdue(vessel, now ?? new Date())) {
    return <Badge tone="alert">Overdue</Badge>
  }
  return <Badge tone={STATUS_TONES[vessel.status]}>{STATUS_LABELS[vessel.status]}</Badge>
}
