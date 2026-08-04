/**
 * Test-only rendering helpers.
 *
 * Nothing in the application imports this segment; it exists so the test
 * suite mounts components under the same providers the app runs with.
 */
import type { ReactElement, ReactNode } from "react"

import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import type { RenderResult } from "@testing-library/react"
import { render } from "@testing-library/react"
import { MemoryRouter } from "react-router-dom"

/**
 * Builds a QueryClient tuned for tests.
 *
 * @returns A client with retries off, so failures surface immediately
 *   instead of being retried into timeouts.
 */
export function createTestQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
}

/**
 * Builds a wrapper component for `renderHook` calls that need a QueryClient.
 *
 * @returns A component wrapping its children in a fresh test QueryClient.
 */
export function createQueryWrapper(): ({ children }: { children: ReactNode }) => ReactElement {
  const queryClient = createTestQueryClient()
  return function QueryWrapper({ children }: { children: ReactNode }): ReactElement {
    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  }
}

/**
 * Renders a component under a fresh QueryClient and a memory router.
 *
 * @param ui - The element under test.
 *
 * @returns The Testing Library render result.
 */
export function renderWithProviders(ui: ReactElement): RenderResult {
  const queryClient = createTestQueryClient()

  function Providers({ children }: { children: ReactNode }): ReactElement {
    return (
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>{children}</MemoryRouter>
      </QueryClientProvider>
    )
  }

  return render(ui, { wrapper: Providers })
}
