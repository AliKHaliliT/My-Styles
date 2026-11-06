import { readFileSync } from "node:fs"
import { resolve } from "node:path"

import { describe, expect, it } from "vitest"

/** The token file as it ships, read from the package root the suite runs in, so the floors are checked on the bytes themselves. */
const css = readFileSync(resolve("src/app/styles/tokens.css"), "utf8")

/** Each theme's block, by the line that opens it. */
const THEMES = { light: ":root {", dark: '[data-theme="dark"] {' }
/** The tokens that carry text, held to the guideline's 4.5:1. */
const TEXT = ["ink", "muted", "signal", "ok", "warn", "alert"]
/** What the text and the controls sit on. */
const BACKGROUNDS = ["surface", "card"]

/** The hex colors a theme block declares, by token name. */
function tokensOf(opener: string): Map<string, string> {
  const body = css.split(opener)[1]?.split("}")[0] ?? ""
  return new Map([...body.matchAll(/--([a-z]+): (#[0-9a-f]{6})/gi)].map((match) => [match[1] ?? "", match[2] ?? ""]))
}

/** Relative luminance, as the guideline defines it over sRGB. */
function luminance(hex: string): number {
  const channel = (at: number): number => {
    const value = Number.parseInt(hex.slice(at, at + 2), 16) / 255
    return value <= 0.03928 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4
  }
  return 0.2126 * channel(1) + 0.7152 * channel(3) + 0.0722 * channel(5)
}

/** The contrast ratio between two colors, from 1 to 21. */
function contrast(a: string, b: string): number {
  const first = luminance(a)
  const second = luminance(b)
  return (Math.max(first, second) + 0.05) / (Math.min(first, second) + 0.05)
}

/** A token the block must declare, or the test fails on its absence rather than on arithmetic over nothing. */
function token(tokens: Map<string, string>, name: string): string {
  const value = tokens.get(name)
  if (value === undefined) throw new Error(`the token file declares no --${name}`)
  return value
}

describe("the design tokens", () => {
  for (const [theme, opener] of Object.entries(THEMES)) {
    it(`clears the contrast floors in the ${theme} theme`, () => {
      const tokens = tokensOf(opener)
      for (const background of BACKGROUNDS) {
        const behind = token(tokens, background)
        for (const name of TEXT) {
          expect(contrast(token(tokens, name), behind), `${name} on ${background}`).toBeGreaterThanOrEqual(4.5)
        }
        expect(contrast(token(tokens, "edge"), behind), `edge on ${background}`).toBeGreaterThanOrEqual(3)
      }
    })
  }
})
