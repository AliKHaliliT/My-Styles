# 0149. Let the tooling see the suites and ports an engine carries

Status: Accepted
Date: 2026-11-25

## Context

The engines layout gives each engine its own ports and suites inside its
folder, and the engines README said that a first engine's paths join the
type-check command and its clause joins the import contract. A project
built from this style added a first engine and found the rest of the
tooling blind to it. The suite run collected the root's `tests` folder
alone, so the engine's suites never ran. The lint's ignores named only
the app's suites and ports, so the engine's suites failed on their
asserts and missing docstrings and its ports on their one-line stubs.
The docs audit's seams check read only paths under `tests/`, so an
engine suite could patch a module and pass every check the gate runs.

## Evidence

Read on 2026-11-25 at 05a5f80. The suite run's paths named `tests`
alone, the lint's ignores named `tests/**` and the app's ports alone,
and the seams check skipped every path that did not begin with `tests/`.
The template carries no engine, its engines folder holding only its
README, so no check ever met an engine's files.

## Options considered

- Adding an engine's paths to each tool when the first engine lands, as
  the README said of the type-check command. Refused, because a step a
  project must remember at that moment is one it forgets, as the
  reporting project did, and a path that names an empty folder costs
  nothing until then.
- Holding the configuration by a test of its text. Refused, because a
  check of the text holds the words and not what the suite run and the
  lint make of an engine.

## Decision

The suite run collects `engines` beside `tests`, the lint's ignores give
an engine's suites and ports the codes the app's carry, and the docs
audit's seams check reads every tracked file in a folder named `tests`,
the root's or one an engine carries, in all three copies of the Python
audit, with a plant under an engine's `tests` folder. The engines README
says so. The type-check command still waits for the first engine,
because the type checker refuses a folder that holds no source. A case
builds an engine in a scratch folder beside a copy of the project's
configuration and asks the suite run what it collects and the lint what
it makes of the engine's suites and ports, and the ledger gains the
claim. Four breaks, each one point, each failed a case or the audit's
plant.

## Consequences

A project's first engine has its suites run, its suites and ports linted
as the app's are, and its suites held to the seams rule from the day it
lands.
