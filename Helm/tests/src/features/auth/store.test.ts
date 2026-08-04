import { describe, expect, it } from "vitest"

import { useAuthStore } from "@/features/auth"

describe("useAuthStore", () => {
  it("holds the session between signIn and signOut", () => {
    useAuthStore.getState().signIn({ token: "t1", displayName: "Harbormaster Ashcroft" })
    expect(useAuthStore.getState().session?.displayName).toBe("Harbormaster Ashcroft")

    useAuthStore.getState().signOut()
    expect(useAuthStore.getState().session).toBeNull()
  })

  it("persists the session to sessionStorage so a refresh survives", () => {
    useAuthStore.getState().signIn({ token: "t2", displayName: "Harbormaster Ashcroft" })
    const stored = sessionStorage.getItem("helm-session")
    expect(stored).not.toBeNull()
    expect(stored).toContain("t2")
    useAuthStore.getState().signOut()
  })
})
