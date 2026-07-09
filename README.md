# kvstore

This repo is a small Redis-backed key-value store with a Python CLI.

## Usage

Start Redis:

```sh
docker compose -f compose.yml up -d
```

Install dependencies and run commands with `uv`:

```sh
uv sync
uv run kvstore --help
```

Set a key with the default 60-second TTL:

```sh
uv run kvstore set my-key my-value
```

Set a key with a custom TTL in seconds:

```sh
uv run kvstore set my-key my-value 120
```

Read, delete, and list keys:

```sh
uv run kvstore get my-key
uv run kvstore delete my-key
uv run kvstore list_keys
```

By default the app connects to Redis at `localhost:6379`, database `0`, and stores keys under the `kvstore:` namespace. Override those with `KVSTORE_REDIS_HOST`, `KVSTORE_REDIS_PORT`, `KVSTORE_REDIS_DB`, and `KVSTORE_REDIS_NAMESPACE`.

Run tests:

```sh
uv run python -m unittest
```
