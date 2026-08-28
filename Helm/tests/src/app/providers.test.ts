import { beforeEach, describe, expect, it } from "vitest"

import { queryClient } from "@/app/providers"
import { useAuthStore } from "@/features/auth"
import { ApiError } from "@/shared/api"

const rejection = new ApiError(401, "Sign in to reach the harbor office.")

describe("the app QueryClient's 401 hooks", () => {
  beforeEach(() => {
    useAuthStore.getState().signIn({ token: "stale-token", displayName: "Harbormaster Ashcroft" })
  })

  it("signs out when a query errors with 401", () => {
    queryClient.getQueryCache().config.onError?.(rejection, undefined as never)

    expect(useAuthStore.getState().session).toBeNull()
  })

  it("signs out when a mutation errors with 401", () => {
    queryClient
      .getMutationCache()
      .config.onError?.(rejection, undefined, undefined, undefined as never, undefined as never)

    expect(useAuthStore.getState().session).toBeNull()
  })

  it("leaves the session alone on any other failure", () => {
    queryClient.getQueryCache().config.onError?.(new Error("wire down"), undefined as never)

    expect(useAuthStore.getState().session).not.toBeNull()
  })
})
