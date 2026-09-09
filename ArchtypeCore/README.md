# ArchetypeCore

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A Strict, AI-Ready Clean Architecture Template for FastAPI.

ArchetypeCore is a highly structured backend template built with FastAPI, Async SQLAlchemy, and Pydantic V2. It is designed around **Domain-Driven Design (DDD)** and **Clean Architecture** principles.

## The Philosophy: Why Does This Exist?

AI coding assistants make starting a project fast and keeping its shape hard. As a project grows, they suffer from **"Architecture Drift"**: taking shortcuts, mixing database queries directly into web routes, leaking HTTP exceptions into business logic, and gradually creating technical debt.

ArchetypeCore was built to mitigate this. By enforcing explicit boundaries (Translators, Protocols, Unit of Work), it provides a strict structural foundation that guides AI agents (and developers) toward writing decoupled, maintainable code. An assistant extends whatever pattern it can see, so a tree whose every seam already shows the right pattern makes the next generated route, repository, or service far more likely to land inside it.

This project is a living point of reference for future works, continuously updated and refined as new improvements, modifications, or components prove necessary.

## The Domain Example: Why a VPN Control Plane?

Many architectural templates use generic "To-Do List" or "Blog" examples, which are often too simple to demonstrate how an architecture handles real-world complexity.

To demonstrate the utility of Dependency Inversion, ArchetypeCore implements the domain of a **VPN (WireGuard) Control Plane**.

Managing a VPN forces the architecture to handle practical, complex problems:

- **External System State:** Syncing a local database with an actual OS-level network interface.
- **Abstract Infrastructure:** The business logic coordinates network creation through an abstract `IVPNProvider` interface, so the core never learns which provider implementation it drives.
- **Background Jobs:** It utilizes standalone scripts (`scripts/`) to monitor data usage and enforce quotas without relying on the web framework.

> **Disclaimer on the WireGuard Implementation:**
> While this template is a logically complete VPN manager, its primary purpose is architectural demonstration. The WireGuard subprocess interactions (`wg` / `wg-quick`) are proven against a live interface by `scripts/wg_smoke.py`, but routing under real client traffic is left to each deployment's own validation. Do not deploy the networking components to a production server without thorough networking validation.

---

## Core Architectural Pillars

ArchetypeCore enforces the **Dependency Rule**: inner layers (Business Logic) must not depend on outer layers (Web Frameworks, Databases, OS).

1. **The Unit of Work (UoW) Pattern**  
   Business services do not interact with the database directly. They use the `IUnitOfWork` to group repository actions. If an operation fails midway, the UoW rolls back the entire transaction to prevent partial states.
2. **Strict Translators**  
   API Schemas are strictly for HTTP validation. Database Models are strictly for SQLAlchemy. Data crossing between these layers must be translated into pure Domain Schemas.
3. **Dependency Inversion**  
   Application services (`UserService`, `DeviceService`) depend only on pure Python `Protocols`. The Web Layer handles injecting concrete implementations (like `SQLAlchemyUnitOfWork` or `WireGuardProvider`) at runtime.
4. **Decoupled Exceptions**  
   Business logic raises pure Python exceptions (e.g., `EntityNotFoundError`). A global exception handler intercepts these and translates them into standardized HTTP JSON payloads.

---

## Project Structure

```text
archetype-core/
├── app/                        # Main application code
│   ├── api/                    # Web presentation layer (FastAPI, Routers, API Schemas)
│   ├── core/                   # App-wide infrastructure (Settings, Middlewares, Logging)
│   ├── docs/                   # OpenAPI / Swagger UI custom generators
│   ├── domain/                 # Absolute source of truth (Interfaces, Domain Schemas, Exceptions)
│   ├── i18n/                   # Internationalization files
│   ├── models/                 # Database mapping layer (SQLAlchemy Declarative Models)
│   ├── repositories/           # Concrete DB access and DB Translators
│   ├── services/               # Business logic orchestration
│   ├── static/                 # Files the server serves itself (a co-hosted Helm dashboard lands here)
│   └── utils/                  # General-purpose utilities (e.g., Field Reordering)
│
├── db/                         # Database connection, mixins, and Alembic migrations
├── docs/                       # Technical documentation (indexed in AGENTS.md)
├── engines/                    # Self-contained, framework-free business engines
├── scripts/                    # Background jobs and CLI commands (e.g., Quota Monitors)
├── tests/                      # Automated test suite mirroring root structure
├── AGENTS.md                   # Agent entry point and the documentation index
├── STATE.md                    # Living project state
└── main.py                     # Entrypoint for the FastAPI application
```

---

## Key Features

- **Custom Colored Logging:** Hierarchical ANSI terminal logs via a custom `logging.Formatter` that automatically tracks and injects Request IDs (`x-request-id`).
- **Advanced Security Middlewares:** Pre-configured ASGI middlewares for CORS, Content-Security-Policy (CSP), Strict-Transport-Security (HSTS), and modern Origin Isolation headers.
- **Auto-Generated Swagger Examples:** Pydantic `json_schema_extra` configurations ensure the `/docs` UI shows realistic payload examples without polluting Base Mixins.
- **CLI Operational Scripts:** Standalone Python scripts (`quota_monitor.py`, `peer_sync.py`) that successfully hook into the database and domain logic without booting up the web server.
- **A Dashboard Slot, Not a Dashboard:** A UI beside this server is a [Helm](https://github.com/AliKHaliliT/My-Styles/tree/main/Helm) instance. Its build output lands in the app's `static/` slot and is served under a prefix with single-page fallback while the API keeps `/api/v1`, so one image ships both; the same build also runs standalone on any static host. Helm's source stays in its own tree under its own law, and this server serves the artifact and never imports it.

---

## Getting Started

### 1. Local Development (Python)

Ensure you have Python 3.14+ installed.

```bash
# Clone the repository
git clone https://github.com/AliKhaliliT/YOUR_REPO.git
cd archetype-core

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Create an initial Admin user (Interactive CLI)
python scripts/create_admin.py

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Navigate to [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs) to view the API documentation.

### 2. Docker Deployment

The project includes a `Dockerfile` and `docker-compose.yml` configured to request the `NET_ADMIN` privileges required for VPN interface manipulations.

```bash
docker-compose up --build -d
```

_(Note: The `entrypoint.sh` automatically handles Alembic migrations upon container startup)._

---

## Conventions

The project's conventions live in one place, the rulebook at [docs/CONVENTIONS.md](docs/CONVENTIONS.md). It holds the documentation system (a vendor-neutral [AGENTS.md](AGENTS.md) as the agent entry point and the single index of every document, [STATE.md](STATE.md) as the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) as the current map, and immutable decision records under [docs/decisions/](docs/decisions/) as the reasoning behind every settled choice), the docstring convention in its code-level section, and the prose law in its Prose section. That file is normative and must not be modified; the rationale behind the system itself is recorded in the style's founding decision record, 0001.

The rulebook is owned at the style level. A project built from this template never changes it locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; the project's `UPSTREAM.md` carries it back to the template as [AGENTS.md](AGENTS.md) describes, where it is verified and, if it holds, adopted for every project that follows the style.

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.
