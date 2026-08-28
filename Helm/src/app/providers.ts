/**
 * App-level wiring between the layers.
 *
 * This module is where the dependency rule gets its knot tied. The shared
 * client cannot know about the auth feature, so the app layer, which may
 * import both, hands the session lookup down at bootstrap.
 */
import { MutationCache, QueryCache, QueryClient } from "@tanstack/react-query"

import { useAuthStore } from "@/features/auth"
import { ApiError, setTokenProvider } from "@/shared/api"

/**
 * Signs the user out when the backend rejects a call as unauthenticated.
 *
 * @param error - Whatever the cache caught; only a 401 `ApiError` acts.
 *
 * @returns Nothing. The route guard walks the signed-out user to login.
 */
function signOutOn401(error: unknown): void {
  if (error instanceof ApiError && error.status === 401) {
    useAuthStore.getState().signOut()
  }
}

/**
 * The application QueryClient.
 *
 * A 401 from any query or mutation means the session died server-side, so
 * both cache error hooks sign the user out.
 */
export const queryClient = new QueryClient({
  queryCache: new QueryCache({ onError: signOutOn401 }),
  mutationCache: new MutationCache({ onError: signOutOn401 }),
})

/**
 * Points the shared HTTP client at the auth store for bearer tokens.
 *
 * @returns Nothing. Called once at bootstrap, before any request can fire.
 */
export function wireTokenProvider(): void {
  setTokenProvider(() => useAuthStore.getState().session?.token ?? null)
}
