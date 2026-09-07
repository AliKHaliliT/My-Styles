import { screen } from "@testing-library/react"
import { beforeEach, describe, expect, it } from "vitest"

import { issueToken } from "@/mocks/db"
import { VesselDetailPage } from "@/pages/vessel-detail"
import { setTokenProvider } from "@/shared/api"
import { renderWithProviders } from "@/shared/testing"

describe("VesselDetailPage", () => {
  beforeEach(() => {
    const token = issueToken()
    setTokenProvider(() => token)
  })

  it("reads the vessel id from the address and renders that vessel's record", async () => {
    renderWithProviders(<VesselDetailPage />, { path: "/vessels/:id", at: "/vessels/v1" })

    expect(await screen.findByRole("heading", { name: "Gull of Brine" })).toBeInTheDocument()
    expect(screen.getByText("Salt")).toBeInTheDocument()
  })

  it("refuses an address that carries no vessel id", () => {
    renderWithProviders(<VesselDetailPage />, { path: "/vessels" })

    expect(screen.getByText("No vessel id in the address.")).toBeInTheDocument()
  })

  it("shows the backend's reason when the vessel is not on the books", async () => {
    renderWithProviders(<VesselDetailPage />, { path: "/vessels/:id", at: "/vessels/nobody" })

    expect(await screen.findByText("No vessel with that id is on the books.")).toBeInTheDocument()
  })
})
