import { z } from "zod"

import { request } from "@/shared/api"

import type { Session } from "./store"

const sessionDtoSchema = z.object({
  token: z.string(),
  display_name: z.string(),
})

/** What the login form collects. */
export interface Credentials {
  username: string
  password: string
}

/**
 * Exchanges credentials for a session.
 *
 * @param credentials - Username and password as entered.
 *
 * @returns The session the backend issued.
 */
export async function loginRequest(credentials: Credentials): Promise<Session> {
  const dto = await request("/auth/session", sessionDtoSchema, {
    method: "POST",
    body: { username: credentials.username, password: credentials.password },
  })
  return { token: dto.token, displayName: dto.display_name }
}
