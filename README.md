# CodeChallengeSDK

A small Python SDK that wraps a few endpoints of the public [Jikan v4 API](https://docs.api.jikan.moe/) (unofficial MyAnimeList REST API), stores fetched results in an in-memory data store with full CRUD, and exposes a thin service layer that ties the two together.

## Project structure

```text
src/
├── main.py                       # Demo entry point
├── sdk_challenge/
│   ├── __init__.py
│   ├── api_client.py             # JikanAPIClient — HTTP client (3 endpoints)
│   ├── storage.py                # AnimeInfo dataclass + AnimeInfoStorage (CRUD)
│   └── service.py                # AnimeService — orchestrates client + storage
└── tests/
    ├── conftest.py
    ├── debug_helpers.py
    ├── test_api.py               # Live API tests
    └── test_crud.py              # Storage CRUD tests
setup.cfg                         # flake8 / mypy / isort config
requirements.txt                  # Runtime deps
requirements-dev.txt              # Linters + test deps
```

## Components

- **`JikanAPIClient`** — exposes three endpoints: `get_anime_info(id)`, `search_anime(query)`, `get_top_anime()`. Each call returns `(success: bool, payload: dict)`.
- **`AnimeInfoStorage`** — in-memory dict keyed by anime id with `save` / `load` / `update` / `delete` / `print_storage`.
- **`AnimeService`** — calls the client, maps the raw payload to an `AnimeInfo` dataclass, and persists it through the storage.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Run the demo

```bash
PYTHONPATH=src python3 src/main.py
```

This fetches One Piece by id, runs a search for "Naruto", and dumps the resulting in-memory storage to the log.

## Tests

```bash
PYTHONPATH=src pytest src/tests
```

Note: `test_api.py` performs live HTTP calls to `api.jikan.moe`; an internet connection is required and the public API rate-limits to ~3 req/s.

## Linters

The project must pass both `mypy` (strict, per `setup.cfg`) and `flake8` with [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide).

```bash
python3 -m mypy src/
python3 -m flake8 src/
```

Both should report zero errors.

## Changelog

### v1.1 — iteration on code-review feedback

**Storage keying (CRUD fully reachable)**

The original `_to_anime_info` helper in `service.py` minted a fresh `uuid4()` on every call,
meaning each fetch of the same anime produced a separate record and `update`/`delete` were
unreachable through the service. The key is now the natural primary key — `mal_id` (the
MyAnimeList integer ID). `AnimeInfoStorage` is typed `Dict[int, AnimeInfo]` accordingly, and
`AnimeInfo` no longer carries a `uuid` field.

**CRUD tests rewritten**

`test_crud.py` was rewritten to exercise the full create → read → update → delete cycle against
real `AnimeInfo` / `AnimeInfoStorage` objects. Magic numbers were extracted to named constants
(`ONE_PIECE_ID`, `INITIAL_RATING`, etc.) so the intent of each assertion is self-documenting.
Type annotations were added to all helper functions (`test_read`, `test_update`, `test_delete`)
to satisfy the strict mypy config.

**Linter now actually passes**

`flake8` and `mypy` both report zero errors across all 11 source files.

```bash
~/dev/git/CodeChallengeSDK main*
❯ python3 -m flake8 src/ 2>&1 && echo "flake8: OK" && python3 -m mypy src/ 2>&1
flake8: OK
Success: no issues found in 11 source files

```

Both should report zero errors.
