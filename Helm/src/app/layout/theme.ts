/**
 * The color theme, as client state.
 *
 * The store holds the current choice, the DOM carries it as a `data-theme`
 * attribute the tokens file keys on, and localStorage remembers it across
 * visits. `initTheme` runs at bootstrap so the first paint is already right.
 */
import { create } from "zustand"

export type Theme = "light" | "dark"

interface ThemeState {
  theme: Theme
  toggleTheme: () => void
}

const STORAGE_KEY = "helm-theme"

/**
 * Stamps the theme onto the document root for the token file to key on.
 *
 * @param theme - The theme to apply.
 *
 * @returns Nothing.
 */
function applyTheme(theme: Theme): void {
  document.documentElement.dataset["theme"] = theme
}

/**
 * Reads a previously stored choice.
 *
 * @returns The stored theme, or null when absent or unrecognizable.
 */
function readStoredTheme(): Theme | null {
  const raw = localStorage.getItem(STORAGE_KEY)
  return raw === "dark" || raw === "light" ? raw : null
}

/**
 * Asks the operating system which theme it prefers.
 *
 * @returns The system preference.
 */
function preferredTheme(): Theme {
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
}

export const useTheme = create<ThemeState>()((set, get) => ({
  theme: "light",
  toggleTheme: () => {
    const next: Theme = get().theme === "dark" ? "light" : "dark"
    localStorage.setItem(STORAGE_KEY, next)
    applyTheme(next)
    set({ theme: next })
  },
}))

/**
 * Resolves the initial theme and applies it, before first render.
 *
 * @returns Nothing.
 */
export function initTheme(): void {
  const theme = readStoredTheme() ?? preferredTheme()
  applyTheme(theme)
  useTheme.setState({ theme })
}
