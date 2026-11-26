import { HttpResponse, http } from "msw"
import { describe, expect, it, vi } from "vitest"

import { berthListDtoSchema } from "@/entities/berth/dto"
import { ApiError, WireContractError, request } from "@/shared/api"
import { server } from "@/mocks/node"

describe("request", () => {
  it("turns a refusal in the family's envelope into an ApiError carrying its detail", async () => {
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

  it("reads a plain backend's message field when the body carries no detail", async () => {
    server.use(
      http.get("/api/berths", () => {
        return HttpResponse.json({ message: "The berth ledger is closed for the night." }, { status: 503 })
      }),
    )

    await expect(request("/berths", berthListDtoSchema)).rejects.toSatisfy((error: unknown) => {
      return error instanceof ApiError && error.status === 503 && error.message === "The berth ledger is closed for the night."
    })
  })

  it("falls back to the title when a validation refusal lists its reasons under detail", async () => {
    server.use(
      http.get("/api/berths", () => {
        return HttpResponse.json(
          {
            title: "Validation Error",
            detail: [{ loc: ["query", "page"], msg: "Input should be a valid integer" }],
            status_code: 422,
            type: "validation_error",
          },
          { status: 422 },
        )
      }),
    )

    await expect(request("/berths", berthListDtoSchema)).rejects.toSatisfy((error: unknown) => {
      return error instanceof ApiError && error.status === 422 && error.message === "Validation Error"
    })
  })

  it("sends a PUT, the method a backend may take a whole record's replacement by", async () => {
    server.use(
      http.put("/api/berths", () => {
        return HttpResponse.json([])
      }),
    )

    await expect(request("/berths", berthListDtoSchema, { method: "PUT", body: [] })).resolves.toEqual([])
  })

  it("ends a request its caller aborts, and the request rejects with the AbortError", async () => {
    let started = (): void => {}
    const handlerStarted = new Promise<void>((resolve) => {
      started = resolve
    })
    let ended = false
    server.use(
      http.get("/api/berths", async ({ request: held }) => {
        started()
        await new Promise<void>((resolve) => {
          held.signal.addEventListener("abort", () => {
            resolve()
          })
        })
        ended = true
        return HttpResponse.json([])
      }),
    )
    const controller = new AbortController()

    const pending = request("/berths", berthListDtoSchema, { signal: controller.signal })
    await handlerStarted
    controller.abort()

    await expect(pending).rejects.toMatchObject({ name: "AbortError" })
    await vi.waitFor(() => {
      expect(ended).toBe(true)
    })
  })

  it("falls back to the status line when the body is not JSON", async () => {
    server.use(
      http.get("/api/berths", () => {
        return HttpResponse.text("gateway down", { status: 502, statusText: "Bad Gateway" })
      }),
    )

    await expect(request("/berths", berthListDtoSchema)).rejects.toSatisfy((error: unknown) => {
      return error instanceof ApiError && error.status === 502 && error.message === "Bad Gateway"
    })
  })
})
