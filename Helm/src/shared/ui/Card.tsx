import type { HTMLAttributes } from "react"

import { cn } from "@/shared/lib"

/** The standard raised container for a block of content. */
export function Card({ className, ...rest }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn("rounded-lg border border-line bg-card p-5", className)} {...rest} />
}
