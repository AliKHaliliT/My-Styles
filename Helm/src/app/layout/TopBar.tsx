import { NavLink, useNavigate } from "react-router-dom"

import { useAuthStore } from "@/features/auth"
import { cn } from "@/shared/lib"
import { Button } from "@/shared/ui"

import { useTheme } from "./theme"

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/vessels", label: "Vessels", end: false },
  { to: "/schedule", label: "Schedule", end: false },
]

/** The persistent header: identity, navigation, theme, and session. */
export function TopBar() {
  const session = useAuthStore((state) => state.session)
  const signOut = useAuthStore((state) => state.signOut)
  const navigate = useNavigate()
  const theme = useTheme((state) => state.theme)
  const toggleTheme = useTheme((state) => state.toggleTheme)

  return (
    <header className="border-b border-line bg-card">
      <div className="mx-auto flex w-full max-w-4xl items-center gap-6 px-4 py-3">
        <span className="text-lg font-semibold text-ink" aria-label="Helm">
          ⎈ Helm
        </span>
        {session !== null ? (
          <nav className="flex gap-4 text-sm">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) => cn("text-muted hover:text-ink", isActive && "font-medium text-signal")}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        ) : null}
        <div className="ml-auto flex items-center gap-3">
          <Button variant="ghost" onClick={toggleTheme} aria-label="Toggle color theme">
            {theme === "dark" ? "Light" : "Dark"}
          </Button>
          {session !== null ? (
            <>
              <span className="text-sm text-muted">{session.displayName}</span>
              <Button
                variant="ghost"
                onClick={() => {
                  signOut()
                  void navigate("/login")
                }}
              >
                Sign out
              </Button>
            </>
          ) : null}
        </div>
      </div>
    </header>
  )
}
