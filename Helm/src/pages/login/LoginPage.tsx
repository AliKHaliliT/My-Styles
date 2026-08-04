import { useLocation, useNavigate } from "react-router-dom"

import { LoginForm } from "@/features/auth"
import { Card } from "@/shared/ui"

/**
 * The sign-in page.
 *
 * When the auth guard sent the visitor here, it left the wanted location in
 * router state; a successful login returns them to it.
 */
export function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: { pathname?: string } } | null)?.from?.pathname ?? "/"

  return (
    <div className="mx-auto max-w-sm py-16">
      <Card>
        <h1 className="mb-1 text-xl font-semibold text-ink">Port of Saltmere</h1>
        <p className="mb-6 text-sm text-muted">Sign in to the harbormaster console.</p>
        <LoginForm
          onSignedIn={() => {
            void navigate(from, { replace: true })
          }}
        />
        <p className="mt-6 text-xs text-muted">Demo credentials: username "harbormaster", password "saltmere".</p>
      </Card>
    </div>
  )
}
