import { Outlet } from "react-router-dom"

import { TopBar } from "./TopBar"

/** The chrome around every page: bar on top, content in a centered column. */
export function AppLayout() {
  return (
    <div className="min-h-screen bg-surface text-ink">
      <TopBar />
      <main className="mx-auto w-full max-w-4xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}
