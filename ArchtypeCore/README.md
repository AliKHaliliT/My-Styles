# ArchetypeCore

![License](https://img.shields.io/github/license/AliKHaliliT/My-Styles) ![Last Commit](https://img.shields.io/github/last-commit/AliKHaliliT/My-Styles) ![Open Issues](https://img.shields.io/github/issues/AliKHaliliT/My-Styles)

A Strict, AI-Ready Clean Architecture Template for FastAPI.

ArchetypeCore is a highly structured backend template built with FastAPI, Async SQLAlchemy, and Pydantic V2. It is designed around **Domain-Driven Design (DDD)** and **Clean Architecture** principles.

## The Philosophy: Why Does This Exist?

In the era of AI coding assistants (Copilot, ChatGPT, Claude), starting a project is incredibly fast. However, as projects grow, AI assistants often suffer from **"Architecture Drift"**: taking shortcuts, mixing database queries directly into web routes, leaking HTTP exceptions into business logic, and gradually creating technical debt.

ArchetypeCore was built to mitigate this. By enforcing explicit boundaries (Translators, Protocols, Unit of Work), it provides a strict structural foundation that guides AI agents (and developers) toward writing decoupled, maintainable code. Because AI systems excel at pattern recognition, providing a solid structure from the beginning ensures that even when adding large architectural components, the agent is highly likely to follow the established conventions.

AI is inherently stochastic, meaning nothing is perfectly deterministic and there is always a chance an agent might generate messy code. However, the cleaner the foundation, the higher the probability that the resulting codebase remains pristine. On that note, this project will serve as a living point of reference for future works, continuously updated and refined as new improvements, modifications, or components prove necessary.

## The Domain Example: Why a VPN Control Plane?

Many architectural templates use generic "To-Do List" or "Blog" examples, which are often too simple to demonstrate how an architecture handles real-world complexity.

To demonstrate the utility of Dependency Inversion, ArchetypeCore implements the domain of a **VPN (WireGuard) Control Plane**.

Managing a VPN forces the architecture to handle practical, complex problems:

- **External System State:** Syncing a local database with an actual OS-level network interface.
- **Abstract Infrastructure:** The business logic coordinates network creation using an abstract `IVPNProvider` interface, demonstrating that the core application remains framework-agnostic.
- **Background Jobs:** It utilizes standalone scripts (`scripts/`) to monitor data usage and enforce quotas without relying on the web framework.

> ⚠️ **Disclaimer on the WireGuard Implementation:**
> While this template acts as a logically complete VPN manager, it serves primarily as an **architectural demonstration**. The WireGuard subprocess interactions (`wg` / `wg-quick`) are theoretical examples of the `IVPNProvider` interface and are **untested in a live routing environment**. Do not deploy the networking components to a production server without thorough networking validation.

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
│   ├── static/                 # Static web assets
│   ├── templates/              # HTML templates (Jinja2)
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

---

## Getting Started

### 1. Local Development (Python)

Ensure you have Python 3.13+ installed.

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

Documentation follows the **NumPy docstring style**, with one house addition: classes carry a `Usage` block (not part of the NumPy standard) that holds a minimal, runnable end-to-end example. `Usage` is not a replacement for NumPy's `Examples` section; the two serve different purposes (`Usage` shows the one canonical way to construct and drive the component, whereas `Examples` illustrates specific behaviors or edge cases), and `Examples` may still be added wherever it is warranted. Where a function warrants a full docstring, all three of `Parameters`, `Returns`, and `Raises` are always present, using the `None.` sentinel when a section is empty (no arguments, or nothing raised); `Raises` otherwise lists every exception raised directly in the body, including the defensive argument-validation guards.

Not everything is documented that heavily, by design. Purely internal helpers and thin mappers keep a one-line summary, and the API layer omits `Parameters`/`Returns`/`Raises` because its contract is already expressed through the Pydantic schemas, the OpenAPI docs, and the global exception handlers.

The rest of the NumPy vocabulary is used where it fits and omitted where it does not: a caveat becomes a `Notes` section (see the middleware classes) rather than a loose sentence, a generator would document `Yields`, a `warnings.warn` would document `Warns`, and `See Also`/`References` are there for cross-references. Sections you do not see are simply not called for by that code; generated code should add them as it introduces the behavior.

Beyond docstrings, the project's technical documentation is governed by a fixed documentation system: a vendor-neutral [AGENTS.md](AGENTS.md) serves as the agent entry point and the single index of every document, [STATE.md](STATE.md) tracks the living project state, [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) holds the current map of the system, and immutable decision records under [docs/decisions/](docs/decisions/) hold the reasoning behind every settled choice. The full rulebook, including the split between living documents and records and the writing rules for each species, lives in [docs/CONVENTIONS.md](docs/CONVENTIONS.md); that file is normative and must not be modified. The rationale behind the system itself is recorded in [its founding decision record](docs/decisions/0001-adopt-the-documentation-system.md).

Both the rulebook and the conventions above are owned at the style level. A project built from this template never changes them locally, and an improvement discovered while refactoring against the template is not kept as a private advantage; [AGENTS.md](AGENTS.md) describes the upstream report that carries it back to the template, where it is verified and, if it holds, adopted for every project that follows the style.

One further rule applies to every piece of prose in the project, from this README through docstrings to commit messages. Everything must read as if a person wrote it. The clearest machine tell is the clause-colon splice, a sentence shaped as claim, colon, elaboration; no human writes that way outside a slide deck, so in prose a colon may only introduce a list, a quote, or a label. Softer tells, such as a balanced semicolon antithesis or a neat triadic list, are each fine on their own but give the text away when stacked, because a paragraph of polished epigrams reads as machine writing even when every sentence would pass alone. Allow at most one such flourish per paragraph and write the rest as plain declarative sentences.

One rule governs string delimiters in code, and it is general on purpose. Where a language offers a free choice of delimiter with identical semantics, use double quotes, switching only where it avoids escapes; where the delimiters differ in meaning, as they do in SQL or a shell, the meaning decides. The rule binds only where the choice is actually free, which is what lets it hold in every language the family touches without ever fighting a syntax, and where a checker for it exists, the Lint verb carries it.

---

## License

This work is under an [MIT](https://choosealicense.com/licenses/mit/) License.
