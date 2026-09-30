import { get } from "node:https"

import { describe, expect, it } from "vitest"

/** The words the mock server refuses with, the same at every entrance a Node test can take. */
const refusal = 'Cannot bypass a request when using the "error" strategy'

describe("the mock server", () => {
  it("refuses a fetch that would leave the loopback", async () => {
    await expect(fetch("https://example.invalid/")).rejects.toSatisfy((error: unknown) => {
      return error instanceof Error && error.message.includes(refusal)
    })
  })

  it("refuses a request through a function imported by name from the Node HTTPS module", async () => {
    const outcome = await new Promise<string>((resolve) => {
      get("https://example.invalid/", (response) => resolve(`answered ${String(response.statusCode)}`)).on("error", (error: Error) => resolve(error.message))
    })
    expect(outcome).toContain(refusal)
  })
})
