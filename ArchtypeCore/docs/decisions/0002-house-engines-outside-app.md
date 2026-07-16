# 0002. House business engines outside the app directory

Status: Accepted
Date: 2026-07-16

## Context

The template originally carried a vestigial `src/standalone_package_name/` stub as the placeholder for complex internal components. When the need emerged to host one or more package-sized internal engines (self-contained business cores with Keel-like internals), the stub raised two questions: where such engines should live, and what their folder should honestly be called. The deciding constraint is that this template is a framework- and language-agnostic server blueprint: `app/` is the delivery layer that gets rewritten when the framework or language changes, making it the least portable code in the repository, while an engine, being pure business logic behind explicit ports, is the most portable.

## Options considered

- **Nest engines inside `app/` (for example `app/engines/`).** Rejected: it pollutes the server-only delivery layer, buries the most portable code inside the least portable folder, and makes a framework swap drag the engines along with it.
- **Keep a top-level `src/` folder holding the engines.** Rejected: `src/` signals the src layout of an installable distribution, which these embedded, non-distributed cores are not; the name is dishonest about what the folder contains.
- **A top-level `engines/` directory beside `app/`.** Accepted: honest name, portable code kept separable, and the dependency arrow stays visible in the tree.

## Decision

Engines live in a top-level `engines/` directory as siblings of `app/`, one self-contained folder per engine carrying its own `domain`, `services`, `adapters`, `facade`, and `tests`. The dependency arrow points one way only: `app` depends on an engine exclusively through its `facade`, and an engine never imports from `app/` or the framework. The `src/standalone_package_name/` stub was removed. The internal structure of an engine follows the Keel template.

## Consequences

A framework or language change replaces `app/` while the engines survive untouched, and one engine can be driven by several delivery layers (an HTTP API, a CLI, a queue worker) without any of them reaching into another's folder. The cost is that each engine must police its own boundary: nothing inside an engine may import from `app/`, and the app may touch an engine only through its facade.
