import { screen } from "@testing-library/react"
import { http } from "msw"
import { beforeEach, describe, expect, it } from "vitest"

import { issueToken } from "@/mocks/db"
import { server } from "@/mocks/node"
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

  it("refuses an address that carries no vessel id and asks the backend nothing", async () => {
    const asked: string[] = []
    // Seen first and answering nothing, so each request is noted and passes on to the demo's own handlers.
    server.use(
      http.all("*", ({ request }) => {
        asked.push(new URL(request.url).pathname)
      }),
    )

    renderWithProviders(<VesselDetailPage />, { path: "/vessels" })

    expect(screen.getByText("No vessel id in the address.")).toBeInTheDocument()
    await new Promise((resolve) => setTimeout(resolve, 50))
    expect(asked).toEqual([])
  })

  it("shows the backend's reason when the vessel is not on the books", async () => {
    renderWithProviders(<VesselDetailPage />, { path: "/vessels/:id", at: "/vessels/nobody" })

    expect(await screen.findByText("No vessel with that id is on the books.")).toBeInTheDocument()
  })
})
