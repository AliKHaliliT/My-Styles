import js from "@eslint/js"
import jsdoc from "eslint-plugin-jsdoc"
import reactHooks from "eslint-plugin-react-hooks"
import reactRefresh from "eslint-plugin-react-refresh"
import sonarjs from "eslint-plugin-sonarjs"
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
    rules: {
      // Where the choice of string delimiter is free, it is double quotes; switching is
      // only for avoiding escapes. Core rules carry this until ESLint 10 retires them,
      // at which point the same two move to the @stylistic plugin.
      quotes: ["error", "double", { avoidEscape: true }],
      "jsx-quotes": ["error", "prefer-double"],
      // The environment is read only through shared/config, and all HTTP goes through
      // shared/api's request; both rules are checked here, with the two homes excepted below.
      "no-restricted-syntax": [
        "error",
        {
          selector: "MemberExpression[object.meta.name='import'][object.property.name='meta'][property.name='env']",
          message: "Read the environment through shared/config, never import.meta.env directly.",
        },
      ],
      "no-restricted-globals": [
        "error",
        { name: "fetch", message: "All HTTP goes through shared/api's request." },
      ],
    },
  },
  {
    files: ["src/shared/config/**", "src/shared/api/**", "vite.config.ts"],
    rules: {
      "no-restricted-syntax": "off",
      "no-restricted-globals": "off",
    },
  },
  {
    // Every export carries a doc comment; the one-sentence minimum is the convention in
    // the README. Suites are exempt by the same rule that keeps them outside the
    // every-export requirement, and they live outside src anyway.
    files: ["src/**/*.{ts,tsx}"],
    plugins: { jsdoc },
    rules: {
      "jsdoc/require-jsdoc": [
        "error",
        {
          publicOnly: true,
          require: {
            ClassDeclaration: true,
            FunctionDeclaration: true,
          },
          contexts: [
            "ExportNamedDeclaration > VariableDeclaration",
            "ExportDefaultDeclaration > ArrowFunctionExpression",
            "ExportNamedDeclaration > TSInterfaceDeclaration",
            "ExportNamedDeclaration > TSTypeAliasDeclaration",
          ],
        },
      ],
    },
  },
  {
    // A local assigned and then immediately returned is a name that says nothing the
    // function's own name did not; inline it. Names that explain an expression stay
    // legal and welcome. Decision 0022 carries the line between the two.
    files: ["src/**/*.{ts,tsx}", "tests/**/*.{ts,tsx}"],
    plugins: { sonarjs },
    rules: {
      "sonarjs/prefer-immediate-return": "error",
    },
  },
  ...layerRules,
)
