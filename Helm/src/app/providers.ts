/**
 * App-level wiring between the layers.
 *
 * This module is where the dependency rule gets its knot tied. The shared
 * client cannot know about the auth feature, so the app layer, which may
 * import both, hands the session lookup down at bootstrap.
 */
import { QueryCache, QueryClient } from "@tanstack/react-query"

import { useAuthStore } from "@/features/auth"
import { ApiError, setTokenProvider } from "@/shared/api"

/**
 * The application QueryClient.
 *
 * A 401 from any query means the session died server-side, so the cache's
 * error hook signs the user out and the route guard walks them to login.
 */
export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => {
      if (error instanceof ApiError && error.status === 401) {
        useAuthStore.getState().signOut()
      }
    },
  }),
})

/**
 * Points the shared HTTP client at the auth store for bearer tokens.
 *
 * @returns Nothing. Called once at bootstrap, before any request can fire.
 */
export function wireTokenProvider(): void {
  setTokenProvider(() => useAuthStore.getState().session?.token ?? null)
}
