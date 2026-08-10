/**
 * The demo harbor's API, one MSW handler per endpoint.
 *
 * Handlers enforce auth and answer in wire shapes, with a little latency so
 * the pending states are visible. Swapping this pretend backend for a real
 * one means flipping VITE_API_MODE; no client code changes.
 */
import { HttpResponse, delay, http } from "msw"

import * as db from "./db"

const LATENCY_MS = 300

/**
 * Pulls the bearer token off a request.
 *
 * @param request - The intercepted request.
 *
 * @returns The token, or null when the header is absent or malformed.
 */
function bearerToken(request: Request): string | null {
  const header = request.headers.get("Authorization")
  return header !== null && header.startsWith("Bearer ") ? header.slice("Bearer ".length) : null
}

function unauthorized(): Response {
  return HttpResponse.json({ message: "Sign in to reach the harbor office." }, { status: 401 })
}

/** The MSW request handlers answering the same HTTP a real backend would. */
export const handlers = [
  http.post("/api/auth/session", async ({ request }) => {
    await delay(LATENCY_MS)
    const body = (await request.json()) as { username?: unknown; password?: unknown }
    const session = db.createSession(
      typeof body.username === "string" ? body.username : "",
      typeof body.password === "string" ? body.password : "",
    )
    if (session === null) {
      return HttpResponse.json({ message: "Wrong username or password." }, { status: 401 })
    }
    return HttpResponse.json(session)
  }),

  http.get("/api/vessels", async ({ request }) => {
    await delay(LATENCY_MS)
    if (!db.isValidToken(bearerToken(request))) {
      return unauthorized()
    }
    return HttpResponse.json(db.listVessels())
  }),

  http.get("/api/vessels/:id", async ({ request, params }) => {
    await delay(LATENCY_MS)
    if (!db.isValidToken(bearerToken(request))) {
      return unauthorized()
    }
    const id = typeof params["id"] === "string" ? params["id"] : ""
    const vessel = db.getVessel(id)
    if (vessel === undefined) {
      return HttpResponse.json({ message: "No vessel with that id is on the books." }, { status: 404 })
    }
    return HttpResponse.json(vessel)
  }),

  http.post("/api/vessels/:id/departure", async ({ request, params }) => {
    await delay(LATENCY_MS)
    if (!db.isValidToken(bearerToken(request))) {
      return unauthorized()
    }
    const id = typeof params["id"] === "string" ? params["id"] : ""
    const current = db.getVessel(id)
    if (current === undefined) {
      return HttpResponse.json({ message: "No vessel with that id is on the books." }, { status: 404 })
    }
    if (current.status !== "moored") {
      return HttpResponse.json({ message: "Only a moored vessel can be recorded as departed." }, { status: 409 })
    }
    const departed = db.departVessel(id)
    if (departed === undefined) {
      return HttpResponse.json({ message: "No vessel with that id is on the books." }, { status: 404 })
    }
    return HttpResponse.json(departed)
  }),

  http.get("/api/berths", async ({ request }) => {
    await delay(LATENCY_MS)
    if (!db.isValidToken(bearerToken(request))) {
      return unauthorized()
    }
    return HttpResponse.json(db.listBerths())
  }),

  http.post("/api/arrivals", async ({ request }) => {
    await delay(LATENCY_MS)
    if (!db.isValidToken(bearerToken(request))) {
      return unauthorized()
    }
    const body = (await request.json()) as {
      vessel_name?: unknown
      flag?: unknown
      eta?: unknown
      cargo?: unknown
    }
    if (
      typeof body.vessel_name !== "string" ||
      body.vessel_name === "" ||
      typeof body.flag !== "string" ||
      body.flag === "" ||
      typeof body.eta !== "string" ||
      Number.isNaN(Date.parse(body.eta))
    ) {
      return HttpResponse.json({ message: "The arrival request is missing required fields." }, { status: 422 })
    }
    const created = db.createArrival({
      vessel_name: body.vessel_name,
      flag: body.flag,
      eta: body.eta,
      cargo: typeof body.cargo === "string" && body.cargo !== "" ? body.cargo : null,
    })
    return HttpResponse.json(created, { status: 201 })
  }),
]
