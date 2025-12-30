# Dev-Ops Ticket Management

## Phase I: CLI Application
A Python CLI application for managing tickets in memory.

## Phase II: Full-Stack Web Application (Coming Soon)
Converting to a full-stack web application with FastAPI backend and Next.js frontend.

## Features

- **In-memory ticket management** - No persistent storage required (Phase I)
- **Rich terminal output** - Beautiful, colored CLI interface
- **Priority levels** - LOW, MED, HIGH
- **Status tracking** - BACKLOG, DONE
- **Full CRUD operations** - Create, read, update, delete tickets

## Tech Stack

### Phase I (CLI)
- Python 3.13
- uv (package manager)
- typer (CLI framework)
- pydantic (data validation)
- rich (terminal formatting)

### Phase II (Full-Stack)
**Backend:**
- FastAPI - High-performance async REST API framework
- Neon Serverless PostgreSQL - Serverless database
- SQLAlchemy (async) - Database ORM with Alembic migrations

**Frontend:**
- Next.js 14+ - React framework with App Router
- shadcn/ui + Tailwind CSS - Beautiful UI components
- TypeScript - Type safety

## Installation

```bash
# Install dependencies
uv sync

# Install development dependencies (for testing)
uv sync --group dev
```

## Quick Demo

Run the demo script to see all features in action:

```bash
uv run python demo.py
```

## Testing

The project includes comprehensive tests using pytest.

### Run All Tests

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage report
uv run pytest --cov=backend --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_models.py
uv run pytest tests/test_storage.py
uv run pytest tests/test_cli.py
```

### Test Coverage

The test suite covers:

- **Model Tests** (`tests/test_models.py`)
  - Ticket model validation
  - Priority and Status enum validation
  - Field requirements and defaults
  - Pydantic validation errors

- **Storage Tests** (`tests/test_storage.py`)
  - **Create**: Ticket creation with various configurations
  - **Read**: Get by ID, list all, filter by status/priority
  - **Update**: Update status and priority
  - **Delete**: Remove tickets from storage
  - Integration tests for complete CRUD cycles

- **CLI Tests** (`tests/test_cli.py`)
  - Command execution
  - Help text validation
  - Error handling
  - Exit codes

### Example Test Output

```bash
$ uv run pytest -v
========================= test session starts ==========================
collected 50+ items

tests/test_models.py::TestPriorityEnum::test_priority_values PASSED
tests/test_models.py::TestStatusEnum::test_status_values PASSED
tests/test_models.py::TestTicketModel::test_ticket_creation_with_all_fields PASSED
...
tests/test_storage.py::TestTicketStorage::test_create_ticket_basic PASSED
tests/test_storage.py::TestTicketStorage::test_get_existing_ticket PASSED
tests/test_storage.py::TestTicketStorage::test_update_status_existing_ticket PASSED
tests/test_storage.py::TestTicketStorage::test_delete_existing_ticket PASSED
...
tests/test_cli.py::TestCreateCommand::test_create_basic_ticket PASSED
tests/test_cli.py::TestCLIHelp::test_main_help PASSED
...

========================== 50 passed in 2.5s ===========================
```

## Project Structure

```
todo1/
├── backend/              # Backend (CLI - Phase I)
│   ├── __init__.py       # Package initialization
│   ├── models.py         # Pydantic models (Ticket, Priority, Status)
│   ├── storage.py        # In-memory storage manager
│   ├── cli.py            # Typer CLI commands with Rich formatting
│   └── main.py           # Entry point
├── tests/
│   ├── __init__.py       # Tests package
│   ├── test_models.py    # Model validation tests
│   ├── test_storage.py   # CRUD operation tests
│   └── test_cli.py       # CLI command tests
├── demo.py               # Demo script
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## Development

This project follows the Spec-Driven Development (SDD) approach with requirements defined in `.specify/memory/devops_feature.md`.

### Development Workflow

1. **Install dependencies**: `uv sync --group dev`
2. **Run tests**: `uv run pytest`
3. **Run demo**: `uv run python demo.py`
4. **Use CLI**: `uv run python -m backend.main [command]`

### Key Design Decisions

- **In-memory storage**: Tickets are stored in memory during runtime (Phase I requirement)
- **Pydantic validation**: All data is validated using Pydantic models
- **Rich formatting**: Terminal output uses Rich library for better UX
- **Type safety**: Full type hints throughout the codebase
- **Comprehensive testing**: 50+ tests covering all CRUD operations
