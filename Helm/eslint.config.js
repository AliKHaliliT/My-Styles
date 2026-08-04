import js from "@eslint/js"
import reactHooks from "eslint-plugin-react-hooks"
import reactRefresh from "eslint-plugin-react-refresh"
import globals from "globals"
import tseslint from "typescript-eslint"

/**
 * The layer rule, enforced rather than reviewed.
 *
 * Each entry names a layer and the layers it may not reach. Cross-slice imports
 * always travel through the "@/" alias, which is what makes them checkable here;
 * a slice's own files use relative paths and are untouched by these patterns.
 */
const LAYERS = [
  { files: ["src/app/**"], forbid: [] },
  { files: ["src/pages/**"], forbid: ["app"] },
  { files: ["src/features/**"], forbid: ["app", "pages"] },
  { files: ["src/entities/**"], forbid: ["app", "pages", "features"] },
  { files: ["src/shared/**"], forbid: ["app", "pages", "features", "entities"] },
]

// A slice is entered through its index.ts, so reaching past one is its own
// violation. Suites are exempt by design and never match these globs.
const DEEP_IMPORT = {
  group: ["@/entities/*/*", "@/features/*/*", "@/pages/*/*", "@/shared/*/*"],
  message: "Enter a slice through its index.ts, not by reaching inside it.",
}

// One rule per layer: ESLint's later config wins for a matching file, so the
// directional patterns and the deep-import pattern have to travel together.
const layerRules = LAYERS.map(({ files, forbid }) => ({
  files,
  rules: {
    "no-restricted-imports": [
      "error",
      {
        patterns: [
          ...forbid.map((layer) => ({
            group: [`@/${layer}`, `@/${layer}/**`],
            message: `Imports point downward only: this layer may not reach @/${layer}.`,
          })),
          DEEP_IMPORT,
        ],
      },
    ],
  },
}))

export default tseslint.config(
  { ignores: ["dist", "public"] },
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      js.configs.recommended,
      ...tseslint.configs.recommended,
      reactHooks.configs.flat["recommended-latest"],
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      ecmaVersion: 2022,
      globals: globals.browser,
    },
  },
  ...layerRules,
)
