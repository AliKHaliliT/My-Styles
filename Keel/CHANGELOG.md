# Changelog

All notable changes to this package are documented in this file, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Entries describe what a consumer of the package needs to know when upgrading; the reasoning behind changes lives in [docs/decisions/](docs/decisions/).

## [Unreleased]

### Changed

- The facade now builds the domain run specification directly from the arguments of `Engine.run`; calls to `Engine.run(goal, max_steps)` behave exactly as before ([decision 0005](docs/decisions/0005-translate-only-outward-at-the-facade-boundary.md)).

### Removed

- The `RunRequest` schema, its `keel.RunRequest` export, and the inbound facade translator. Only code that imported `RunRequest` directly is affected.

## [1.0.0] - 2026-07-14

### Added

- Initial release of the Keel template: the agent-engine demo domain with its bounded reason, act, record loop; the guarded fluent `EngineBuilder`; the deterministic offline `RuleBasedReasoner`; the `AnthropicReasoner` adapter behind the `anthropic` extra; built-in demo tools (calculator, word count, clock); `keel.tools` entry-point discovery for third-party tools; typed `EngineEvent` observability through the `IEventSink` port; and both console-script (`keel`) and `python -m keel` execution.
