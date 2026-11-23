import { HttpResponse, http } from "msw"
import { describe, expect, it } from "vitest"

import { fetchVessel } from "@/entities/vessel/api"
import { vesselDtoSchema } from "@/entities/vessel/dto"
import { server } from "@/mocks/node"
import { WireContractError } from "@/shared/api"

const VESSEL = { id: "v9", name: "Test Vessel", flag: "Norrow", status: "due", eta: "2026-08-10T08:00:00Z", berth_id: null, cargo: "Salt" }

describe("vesselDtoSchema", () => {
  it("refuses an arrival time that carries no offset, which a browser would read as its own local time", () => {
    expect(vesselDtoSchema.safeParse({ ...VESSEL, eta: "2026-08-10T08:00:00" }).success).toBe(false)
  })

  it("refuses an arrival time that is no time at all", () => {
    expect(vesselDtoSchema.safeParse({ ...VESSEL, eta: "not a time" }).success).toBe(false)
  })

  it("takes an arrival time in UTC or with its offset, and no arrival time at all", () => {
    for (const eta of ["2026-08-10T08:00:00Z", "2026-08-10T08:00:00.000Z", "2026-08-10T01:00:00-07:00", null]) {
      expect(vesselDtoSchema.safeParse({ ...VESSEL, eta }).success).toBe(true)
    }
  })

  it("refuses at the boundary a vessel whose arrival time carries no offset", async () => {
    server.use(
      http.get("/api/vessels/v9", () => {
        return HttpResponse.json({ ...VESSEL, eta: "2026-08-10T08:00:00" })
      }),
    )

    await expect(fetchVessel("v9")).rejects.toBeInstanceOf(WireContractError)
  })
})
