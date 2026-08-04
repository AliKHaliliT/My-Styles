import { HttpResponse, http } from "msw"
import { describe, expect, it } from "vitest"

import { berthListDtoSchema } from "@/entities/berth/dto"
import { ApiError, WireContractError, request } from "@/shared/api"
import { server } from "@/mocks/node"

describe("request", () => {
  it("turns a rejection into an ApiError carrying the backend's message", async () => {
    await expect(request("/berths", berthListDtoSchema)).rejects.toSatisfy((error: unknown) => {
      return error instanceof ApiError && error.status === 401 && error.message === "Sign in to reach the harbor office."
    })
  })

  it("refuses a payload that breaks the wire contract", async () => {
    server.use(
      http.get("/api/berths", () => {
        return HttpResponse.json([{ wrong_shape: true }])
      }),
    )

    await expect(request("/berths", berthListDtoSchema)).rejects.toBeInstanceOf(WireContractError)
  })
})
