import { describe, expect, it } from "vitest"

import { arrivalInputToDto, vesselFromDto } from "@/entities/vessel/translate"

describe("vesselFromDto", () => {
  it("maps wire names and revives the ETA into a Date", () => {
    const vessel = vesselFromDto({
      id: "v9",
      name: "Test Vessel",
      flag: "Norrow",
      status: "due",
      eta: "2026-08-10T08:00:00.000Z",
      berth_id: "b2",
      cargo: "Salt",
    })

    expect(vessel.berthId).toBe("b2")
    expect(vessel.eta).toBeInstanceOf(Date)
    expect(vessel.eta?.toISOString()).toBe("2026-08-10T08:00:00.000Z")
  })

  it("keeps nulls null instead of inventing values", () => {
    const vessel = vesselFromDto({
      id: "v9",
      name: "Test Vessel",
      flag: "Norrow",
      status: "departed",
      eta: null,
      berth_id: null,
      cargo: null,
    })

    expect(vessel.eta).toBeNull()
    expect(vessel.berthId).toBeNull()
    expect(vessel.cargo).toBeNull()
  })
})

describe("arrivalInputToDto", () => {
  it("maps domain names to wire names and serializes the ETA", () => {
    const dto = arrivalInputToDto({
      vesselName: "New Caller",
      flag: "Ashvane",
      eta: new Date("2026-08-15T10:30:00.000Z"),
      cargo: null,
    })

    expect(dto.vessel_name).toBe("New Caller")
    expect(dto.eta).toBe("2026-08-15T10:30:00.000Z")
    expect(dto.cargo).toBeNull()
  })
})
