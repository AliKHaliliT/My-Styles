/**
 * The demo harbor's in-memory state.
 *
 * This module is the "database" behind the mock handlers, and it speaks wire
 * shapes only (snake_case keys, ISO strings). The client's schemas and
 * translators are exactly what the demo exercises, so the pretend backend
 * must not share the client's domain types.
 */

interface VesselRow {
  id: string
  name: string
  flag: string
  status: "due" | "moored" | "departed"
  eta: string | null
  berth_id: string | null
  cargo: string | null
}

interface BerthRow {
  id: string
  name: string
  depth_m: number
  occupied_by: string | null
}

const DEMO_USERNAME = "harbormaster"
const DEMO_PASSWORD = "saltmere"

/**
 * Builds an ISO timestamp offset from now, so the seed stays lively no
 * matter when the demo runs.
 *
 * @param hours - Offset in hours; negative values land in the past.
 *
 * @returns The ISO string.
 */
function hoursFromNow(hours: number): string {
  return new Date(Date.now() + hours * 60 * 60 * 1000).toISOString()
}

function seedVessels(): VesselRow[] {
  return [
    { id: "v1", name: "Gull of Brine", flag: "Kestrelmark", status: "moored", eta: null, berth_id: "b1", cargo: "Salt" },
    { id: "v2", name: "Cinder Petrel", flag: "Ashvane", status: "due", eta: hoursFromNow(6), berth_id: null, cargo: "Timber" },
    { id: "v3", name: "Long Meridian", flag: "Vellhaven", status: "due", eta: hoursFromNow(-3), berth_id: null, cargo: "Engine parts" },
    { id: "v4", name: "Quiet Fathom", flag: "Kestrelmark", status: "departed", eta: null, berth_id: null, cargo: null },
    { id: "v5", name: "Iron Cormorant", flag: "Norrow", status: "moored", eta: null, berth_id: "b3", cargo: "Grain" },
  ]
}

function seedBerths(): BerthRow[] {
  return [
    { id: "b1", name: "North Quay", depth_m: 9.5, occupied_by: "v1" },
    { id: "b2", name: "East Pier", depth_m: 7.0, occupied_by: null },
    { id: "b3", name: "Lantern Wharf", depth_m: 11.0, occupied_by: "v5" },
    { id: "b4", name: "South Basin", depth_m: 6.5, occupied_by: null },
  ]
}

let vessels: VesselRow[] = []
let berths: BerthRow[] = []
const tokens = new Set<string>()
let nextId = 0

/**
 * Restores the pristine seed. Tests call this between cases; the browser
 * gets it once at module load.
 *
 * @returns Nothing.
 */
export function resetDb(): void {
  vessels = seedVessels()
  berths = seedBerths()
  tokens.clear()
  nextId = vessels.length + 1
}

/**
 * Mints a valid bearer token, for the login handler and for tests.
 *
 * @returns The token, already registered as valid.
 */
export function issueToken(): string {
  const token = `demo-token-${String(tokens.size + 1)}`
  tokens.add(token)
  return token
}

/**
 * Checks credentials and opens a session.
 *
 * @param username - As entered.
 * @param password - As entered.
 *
 * @returns The wire session payload, or null when the credentials are wrong.
 */
export function createSession(username: string, password: string): { token: string; display_name: string } | null {
  if (username === DEMO_USERNAME && password === DEMO_PASSWORD) {
    return { token: issueToken(), display_name: "Harbormaster Ashcroft" }
  }
  return null
}

/**
 * Judges a bearer token.
 *
 * @param token - The presented token, or null when none was sent.
 *
 * @returns True for a token this session store issued.
 */
export function isValidToken(token: string | null): boolean {
  return token !== null && tokens.has(token)
}

/** Returns every vessel in the pretend database. */
export function listVessels(): VesselRow[] {
  return vessels
}

/** Finds one vessel by id, or undefined when the id is unknown. */
export function getVessel(id: string): VesselRow | undefined {
  return vessels.find((vessel) => vessel.id === id)
}

/** Returns every berth in the pretend database. */
export function listBerths(): BerthRow[] {
  return berths
}

/**
 * Records a new arrival with a fresh id.
 *
 * @param body - The validated wire request.
 *
 * @returns The created vessel row.
 */
export function createArrival(body: { vessel_name: string; flag: string; eta: string; cargo: string | null }): VesselRow {
  const row: VesselRow = {
    id: `v${String(nextId)}`,
    name: body.vessel_name,
    flag: body.flag,
    status: "due",
    eta: body.eta,
    berth_id: null,
    cargo: body.cargo,
  }
  nextId += 1
  vessels.push(row)
  return row
}

/**
 * Marks a vessel departed and frees its berth.
 *
 * @param id - The vessel's identifier.
 *
 * @returns The updated row, or undefined when no such vessel exists.
 */
export function departVessel(id: string): VesselRow | undefined {
  const row = getVessel(id)
  if (row === undefined) {
    return undefined
  }
  if (row.berth_id !== null) {
    const berth = berths.find((candidate) => candidate.id === row.berth_id)
    if (berth !== undefined) {
      berth.occupied_by = null
    }
  }
  row.status = "departed"
  row.berth_id = null
  row.eta = null
  return row
}

// The pretend backend boots seeded, like any demo server would.
resetDb()
