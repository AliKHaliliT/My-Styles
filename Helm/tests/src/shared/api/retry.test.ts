import { describe, expect, it } from "vitest"

import { ApiError, WireContractError, shouldRetry } from "@/shared/api"

describe("shouldRetry", () => {
  it("never asks again after a refusal, since asking brings the same answer back", () => {
    for (const status of [400, 401, 403, 404, 409, 422, 499]) {
      expect(shouldRetry(0, new ApiError(status, "No."))).toBe(false)
    }
  })

  it("never asks again after a payload that broke the contract", () => {
    expect(shouldRetry(0, new WireContractError("/vessels", "eta: Invalid ISO datetime"))).toBe(false)
  })

  it("asks again after the server's own error until three retries are spent", () => {
    for (const status of [500, 503]) {
      const failure = new ApiError(status, "The berth ledger is closed for the night.")
      expect([0, 1, 2, 3].map((count) => shouldRetry(count, failure))).toEqual([true, true, true, false])
    }
  })

  it("asks again after a failure that carried no answer until three retries are spent", () => {
    const failure = new TypeError("Failed to fetch")
    expect([0, 1, 2, 3].map((count) => shouldRetry(count, failure))).toEqual([true, true, true, false])
  })
})
