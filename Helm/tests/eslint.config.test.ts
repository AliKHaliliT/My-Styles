import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

import { ESLint } from "eslint"
import { describe, expect, it, vi } from "vitest"

// The layer rule lives in the lint configuration, so each case hands the linter one import under
// a path of the case's own and reads what the configuration makes of it. The text is linted as
// given, so no case writes a file into the tree.

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)))
const linter = new ESLint({ cwd: ROOT })

// The linter loads the whole configuration on its first call, which outlasts the default wait.
vi.setConfig({ testTimeout: 30_000 })

async function refusals(file: string, specifier: string): Promise<string[]> {
  const text = `import { thing } from "${specifier}"\n\nexport const used = thing\n`
  const results = await linter.lintText(text, { filePath: join(ROOT, file) })
  return results.flatMap((result) =>
    result.messages.filter((message) => message.ruleId === "no-restricted-imports").map((message) => message.message),
  )
}

describe("the layer rule in the lint configuration", () => {
  it.each([
    ["src/pages/alpha/probe.ts", "@/pages/beta"],
    ["src/features/alpha/probe.ts", "@/features/beta"],
    ["src/entities/alpha/probe.ts", "@/entities/beta"],
    ["src/entities/alpha/probe.ts", "@/entities"],
  ])("refuses in %s an import of %s, another slice of its own layer", async (file, specifier) => {
    const found = await refusals(file, specifier)

    expect(found).toHaveLength(1)
    expect(found[0]).toContain("Slices of one layer never import each other")
  })

  it("refuses an import that points up a layer", async () => {
    const found = await refusals("src/entities/alpha/probe.ts", "@/features/beta")

    expect(found).toHaveLength(1)
    expect(found[0]).toContain("Imports point downward only")
  })

  it("refuses an import that reaches past a slice's door", async () => {
    const found = await refusals("src/features/alpha/probe.ts", "@/entities/beta/model")

    expect(found).toHaveLength(1)
    expect(found[0]).toContain("Enter a slice through its index.ts")
  })

  // A layer below, a sibling segment of the shared layer, and a file of the slice's own.
  it.each([
    ["src/features/alpha/probe.ts", "@/entities/beta"],
    ["src/entities/alpha/probe.ts", "@/shared/api"],
    ["src/shared/ui/probe.ts", "@/shared/lib"],
    ["src/entities/alpha/probe.ts", "./model"],
  ])("lets %s import %s", async (file, specifier) => {
    expect(await refusals(file, specifier)).toEqual([])
  })
})
