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
import { MemoryRouter, Route, Routes } from "react-router-dom"

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

/** Options accepted by {@link renderWithProviders}. */
export interface RenderWithProvidersOptions {
  /** Route pattern to mount the element under so it can read route parameters; omitted, the element renders bare. */
  path?: string | undefined
  /** Address the memory router starts at. Defaults to `path`. */
  at?: string | undefined
}

/**
 * Renders a component under a fresh QueryClient and a memory router.
 *
 * Without options the element renders directly inside the router, which is
 * enough for anything that does not read the address. A component that reads
 * route parameters is mounted under `path` with the router started `at` an
 * address the pattern matches, so it reads its parameters the way the app's
 * router hands them over.
 *
 * @param ui - The element under test.
 * @param options - Route pattern and starting address; defaults to a bare mount.
 *
 * @returns The Testing Library render result.
 */
export function renderWithProviders(ui: ReactElement, options: RenderWithProvidersOptions = {}): RenderResult {
  const queryClient = createTestQueryClient()
  const { path, at } = options

  function Providers({ children }: { children: ReactNode }): ReactElement {
    return (
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={[at ?? path ?? "/"]}>
          {path === undefined ? (
            children
          ) : (
            <Routes>
              <Route path={path} element={children} />
            </Routes>
          )}
        </MemoryRouter>
      </QueryClientProvider>
    )
  }

  return render(ui, { wrapper: Providers })
}
