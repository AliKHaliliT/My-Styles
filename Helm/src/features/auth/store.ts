/**
 * The session store.
 *
 * This is client state, not server cache. It lives in Zustand because more
 * than one part of the tree reads it, and it persists to sessionStorage so a
 * refresh does not log the harbormaster out mid-shift.
 */
import { create } from "zustand"
import { createJSONStorage, persist } from "zustand/middleware"

/** An authenticated session as the client holds it. */
export interface Session {
  readonly token: string
  readonly displayName: string
}

interface AuthState {
  session: Session | null
  signIn: (session: Session) => void
  signOut: () => void
}

/** Client store holding the session token and sign-in state, persisted across reloads. */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      session: null,
      signIn: (session) => {
        set({ session })
      },
      signOut: () => {
        set({ session: null })
      },
    }),
    {
      name: "helm-session",
      storage: createJSONStorage(() => sessionStorage),
    },
  ),
)
