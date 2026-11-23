import { QueryObserver } from "@tanstack/react-query"
import { waitFor } from "@testing-library/react"
import { http } from "msw"
import { beforeEach, describe, expect, it } from "vitest"

import { queryClient } from "@/app/providers"
import { fetchVessel } from "@/entities/vessel/api"
import { useAuthStore } from "@/features/auth"
import { issueToken } from "@/mocks/db"
import { server } from "@/mocks/node"
import { ApiError, setTokenProvider } from "@/shared/api"

const rejection = new ApiError(401, "Sign in to reach the harbor office.")

describe("the app QueryClient's retries", () => {
  it("asks a refused query once, so its reason arrives on the first reply", async () => {
    const token = issueToken()
    setTokenProvider(() => token)
    const asked: string[] = []
    // Seen first and answering nothing, so each request is noted and passes on to the demo's own handlers.
    server.use(
      http.all("*", ({ request }) => {
        asked.push(new URL(request.url).pathname)
      }),
    )
    const observer = new QueryObserver(queryClient, { queryKey: ["vessels", "nobody"], queryFn: () => fetchVessel("nobody") })
    const unsubscribe = observer.subscribe(() => undefined)
    try {
      await waitFor(() => {
        expect(observer.getCurrentResult().error).toBeInstanceOf(ApiError)
      })
      expect(asked).toEqual(["/api/vessels/nobody"])
    } finally {
      unsubscribe()
      queryClient.clear()
    }
  })
})

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
