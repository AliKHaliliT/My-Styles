import { renderHook, waitFor } from "@testing-library/react"
import { beforeEach, describe, expect, it } from "vitest"

import { useVessels } from "@/entities/vessel"
import { issueToken } from "@/mocks/db"
import { setTokenProvider } from "@/shared/api"
import { createQueryWrapper } from "@/shared/testing"

describe("useVessels", () => {
  beforeEach(() => {
    const token = issueToken()
    setTokenProvider(() => token)
  })

  it("delivers the seeded fleet as domain models", async () => {
    const { result } = renderHook(() => useVessels(), { wrapper: createQueryWrapper() })

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true)
    })

    const vessels = result.current.data ?? []
    expect(vessels).toHaveLength(5)
    expect(vessels.map((vessel) => vessel.name)).toContain("Gull of Brine")

    const due = vessels.find((vessel) => vessel.name === "Cinder Petrel")
    expect(due?.eta).toBeInstanceOf(Date)
    expect(due?.berthId).toBeNull()
  })
})
