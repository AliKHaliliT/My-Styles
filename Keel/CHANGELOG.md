# Changelog

All notable changes to this package are documented in this file, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Entries describe what a consumer of the package needs to know when upgrading; the reasoning behind changes lives in [docs/decisions/](docs/decisions/).

## [1.0.0] - 2026-07-14

### Added

- Initial release of the Keel template: the agent-engine demo domain with its bounded reason, act, record loop; the guarded fluent `EngineBuilder`; the deterministic offline `RuleBasedReasoner`; the `AnthropicReasoner` adapter behind the `anthropic` extra; built-in demo tools (calculator, word count, clock); `keel.tools` entry-point discovery for third-party tools; typed `EngineEvent` observability through the `IEventSink` port; and both console-script (`keel`) and `python -m keel` execution.
