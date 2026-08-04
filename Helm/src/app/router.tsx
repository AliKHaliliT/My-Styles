import { createBrowserRouter } from "react-router-dom"

import { RequireAuth } from "@/features/auth"
import { env } from "@/shared/config"
import { DashboardPage } from "@/pages/dashboard"
import { LoginPage } from "@/pages/login"
import { NotFoundPage } from "@/pages/not-found"
import { SchedulePage } from "@/pages/schedule"
import { VesselDetailPage } from "@/pages/vessel-detail"
import { VesselsPage } from "@/pages/vessels"

import { AppLayout } from "./layout/AppLayout"

/**
 * The route table, declared in one place.
 *
 * Everything except login and the 404 sits behind the auth guard. The
 * basename follows Vite's base so the build serves correctly from a subpath.
 */
export const router = createBrowserRouter(
  [
    {
      element: <AppLayout />,
      children: [
        {
          element: <RequireAuth />,
          children: [
            { index: true, element: <DashboardPage /> },
            { path: "vessels", element: <VesselsPage /> },
            { path: "vessels/:id", element: <VesselDetailPage /> },
            { path: "schedule", element: <SchedulePage /> },
          ],
        },
        { path: "login", element: <LoginPage /> },
        { path: "*", element: <NotFoundPage /> },
      ],
    },
  ],
  { basename: env.baseUrl },
)
