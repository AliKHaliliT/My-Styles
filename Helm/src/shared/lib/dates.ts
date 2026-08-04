const dateTimeFormatter = new Intl.DateTimeFormat("en-GB", {
  dateStyle: "medium",
  timeStyle: "short",
})

/**
 * Formats a date for display in lists and detail views.
 *
 * @param date - The moment to format.
 *
 * @returns The date in the locale-stable "12 Aug 2026, 14:30" shape.
 */
export function formatDateTime(date: Date): string {
  return dateTimeFormatter.format(date)
}
