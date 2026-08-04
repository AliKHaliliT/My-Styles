import { Navigate, Outlet, useLocation } from "react-router-dom"

import { useAuthStore } from "./store"

/**
 * Route guard for everything behind the sign-in.
 *
 * Mount it as a layout route; children render only with a live session, and
 * anonymous visitors are sent to the login page carrying the location they
 * wanted, so login can return them there.
 */
export function RequireAuth() {
  const session = useAuthStore((state) => state.session)
  const location = useLocation()

  if (session === null) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }

  return <Outlet />
}
