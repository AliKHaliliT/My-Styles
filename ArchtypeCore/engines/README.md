# Engines

This directory holds self-contained business engines: cohesive, framework-free
units built with the same Clean Architecture internals as the rest of the
project (`domain`, `services`, `adapters`, `facade`). Each engine is a portable
core that knows nothing about the web framework, the transport, or the language
runtime it happens to be embedded in.

## Why they live here and not inside `app/`

`app/` is the delivery layer: the part that speaks HTTP and wires up the
framework. It is the layer you rewrite when you move this blueprint to another
framework or language, so it is the least portable code in the repository. An
engine is the opposite: pure business logic behind explicit ports, so it is the
most portable code you own.

Keeping engines as siblings of `app/` rather than nested inside it does two
things. It keeps the dependency arrow pointing the right way (`app` depends on
an engine, never the reverse; an engine never imports from `app/` or the
framework), and it keeps the portable core separable, so a framework swap
replaces `app/` while the engines survive untouched. The same engine can then be
driven by more than one delivery layer (an HTTP API, a CLI, a queue worker)
without any of them reaching into another's folder.

## Layout

One folder per engine, each self-contained down to its own tests:

```text
engines/
└── your_engine/
    ├── domain/        # Pure business logic and port definitions (no framework)
    ├── services/      # Orchestration of the engine's own workflow
    ├── adapters/      # Concrete implementations of the engine's ports
    ├── facade/        # The engine's public surface (the only part app imports)
    └── tests/         # The engine's own tests, so it travels as one unit
```

The delivery layer depends on an engine only through its `facade`, so the
engine's internals stay free to change behind that seam.

For a complete, runnable reference of an engine's internal structure and
conventions, see the `keel` package at the root of this repository.
