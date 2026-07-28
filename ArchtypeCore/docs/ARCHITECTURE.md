# Architecture

This project follows a strict Clean Architecture and Domain-Driven Design (DDD) pattern. The core business logic (`domain` and `services`) is completely isolated from the web framework (`api`) and the database (`repositories`). Business logic that is meant to outlive the framework lives in `engines/` as self-contained, framework-free cores that the app depends on and never the reverse, so a change of framework or language replaces `app/` while the engines survive untouched.

```text
my_project/
├── AGENTS.md                   # Agent entry point and the single documentation index
├── alembic.ini                 # Configuration file for Alembic database migrations
├── app/                        # Main application code
│   ├── api/                    # Web presentation layer (FastAPI specific)
│   │   └── v1/                 # Versioned API
│   │       ├── dependencies/   # FastAPI Depends() injections (auth, db, services)
│   │       ├── routers/        # APIRouter definitions tying endpoint routes together
│   │       ├── routes/         # Actual endpoint logic and path operations
│   │       ├── schemas/        # Pydantic models for API request/response validation
│   │       └── translators/    # Adapters bridging API schemas <-> Domain schemas
│   │
│   ├── core/                   # Application-wide infrastructure and configurations
│   │   ├── config/             # Settings (Pydantic BaseSettings) and env var mapping
│   │   ├── exception_handlers/ # Global FastAPI exception interceptors/formatters
│   │   ├── exceptions/         # Custom HTTP exception definitions
│   │   ├── logging/            # Centralized logging, colored formatters, and request contexts
│   │   ├── middlewares/        # ASGI middlewares (CORS, caching, isolation, security)
│   │   └── security/           # Cryptography, JWT generation, and password hashing
│   │
│   ├── docs/                   # OpenAPI / Swagger UI documentation generation logic
│   │   ├── fragments/          # Markdown fragments injected into docs
│   │   ├── logic/              # Example generators and standardized error payloads
│   │   └── v1/                 # Versioned router documentation responses
│   │
│   ├── domain/                 # Absolute source of truth: Core Business Logic (No frameworks allowed)
│   │   ├── exceptions/         # Pure Python domain-level exceptions
│   │   ├── interfaces/         # Protocols defining contracts (IUnitOfWork, IVPNProvider, etc.)
│   │   └── schemas/            # Pydantic domain models (internal state representations)
│   │
│   ├── i18n/                   # Internationalization and localization files (e.g., .po, .mo)
│   │
│   ├── models/                 # Database mapping layer (SQLAlchemy Declarative Base models)
│   │
│   ├── repositories/           # Database access layer (Implements domain/interfaces)
│   │   ├── sqlalchemy/         # Concrete SQLAlchemy CRUD and Unit of Work implementations
│   │   └── translators/        # Adapters bridging Domain schemas <-> Database models
│   │
│   ├── services/               # Business logic orchestration (Coordinates UoW, Repos, external APIs)
│   │   ├── access/             # Auth, User, and Device management workflows
│   │   └── vpn/                # Concrete VPN protocol implementations (e.g., WireGuardProvider)
│   │
│   ├── static/                 # Static web assets (CSS, JS, images for templates)
│   │
│   ├── templates/              # HTML templates (Jinja2) for potential server-side rendering
│   │
│   └── utils/                  # General-purpose utility functions and decorators (e.g., field reordering)
│
├── backup/                     # Database or file backup storage directory
│
├── db/                         # Database setup and connection management
│   ├── migrations/             # Alembic migration scripts and env setup
│   ├── base.py                 # SQLAlchemy DeclarativeBase initialization
│   ├── mixins.py               # Reusable DB model mixins (e.g., TimestampMixin)
│   └── session.py              # Async engine and session factory setup
│
├── docker-compose.yml          # Docker composition for app and auxiliary services
├── Dockerfile                  # Instructions to build the application container
├── entrypoint.sh               # Startup script for the Docker container (runs migrations, starts uvicorn)
│
├── docs/                       # Technical documentation for maintainers and agents (indexed in AGENTS.md)
│   ├── ARCHITECTURE.md         # This file; the annotated map of the template
│   ├── BASELINE.md             # The repository baseline (always-present files and their rules)
│   ├── CONVENTIONS.md          # The documentation rulebook (frozen; do not edit)
│   └── decisions/              # Immutable decision records; the project's "why" log
│
├── engines/                    # Self-contained, framework-free business engines (portable Clean Architecture cores)
│   └── your_engine/            # One engine per folder; app depends on it only through its facade
│       ├── domain/             # Pure business logic and port definitions (no framework)
│       ├── services/           # Orchestration of the engine's own workflow
│       ├── adapters/           # Concrete implementations of the engine's ports
│       ├── facade/             # The engine's public surface (the only part app imports)
│       └── tests/              # The engine's own tests, so it travels as one unit
│
├── local_util_resources/       # Internal development and repository management scripts
│
├── main.py                     # Entrypoint for the FastAPI application (hooks up routers and middlewares)
├── README.md                   # Project documentation and setup guide
├── requirements.txt            # Python package dependencies
│
├── scripts/                    # Background jobs, CLI commands, and operational scripts
│   ├── backup.sh               # Shell script for automated backups
│   ├── create_admin.py         # CLI tool to securely bootstrap an admin user
│   ├── peer_sync.py            # Cron job to sync VPN interface peers with the DB
│   └── quota_monitor.py        # Cron job to calculate usage and enforce VPN data quotas
│
├── STATE.md                    # Living project state (Now / Next / Deferred / Blocked)
│
├── tests/                      # Automated test suite for the app (mirrors the app structure)
│   └── app/                    # Tests for the main FastAPI application
│       ├── api/                # Integration tests for HTTP endpoints
│       └── services/           # Unit tests for business logic
│
└── util_resources/             # Tracked repository assets
    └── readme/                 # Every image the repository embeds (logo, screenshots, figures)
```
