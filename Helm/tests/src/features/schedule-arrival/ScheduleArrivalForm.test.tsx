import { fireEvent, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { beforeEach, describe, expect, it, vi } from "vitest"

import type { Vessel } from "@/entities/vessel"
import { ScheduleArrivalForm } from "@/features/schedule-arrival"
import { issueToken } from "@/mocks/db"
import { setTokenProvider } from "@/shared/api"
import { renderWithProviders } from "@/shared/testing"

describe("ScheduleArrivalForm", () => {
  beforeEach(() => {
    const token = issueToken()
    setTokenProvider(() => token)
  })

  it("blocks an empty submission with field messages", async () => {
    const onScheduled = vi.fn()
    renderWithProviders(<ScheduleArrivalForm onScheduled={onScheduled} />)

    fireEvent.click(screen.getByRole("button", { name: "Schedule arrival" }))

    expect(await screen.findByText("Name the vessel (at least 2 characters).")).toBeInTheDocument()
    expect(onScheduled).not.toHaveBeenCalled()
  })

  it("schedules a valid arrival and hands the created vessel to the caller", async () => {
    const onScheduled = vi.fn()
    renderWithProviders(<ScheduleArrivalForm onScheduled={onScheduled} />)

    await userEvent.type(screen.getByLabelText("Vessel name"), "New Caller")
    await userEvent.type(screen.getByLabelText("Flag state"), "Ashvane")
    fireEvent.change(screen.getByLabelText("Estimated arrival"), { target: { value: "2026-08-15T10:30" } })

    fireEvent.click(screen.getByRole("button", { name: "Schedule arrival" }))

    await waitFor(() => {
      expect(onScheduled).toHaveBeenCalledTimes(1)
    })

    const created = onScheduled.mock.calls[0]?.[0] as Vessel
    expect(created.name).toBe("New Caller")
    expect(created.status).toBe("due")
    expect(created.cargo).toBeNull()
  })
})
