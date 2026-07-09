import click

from .store import DEFAULT_TTL_SECONDS, KVStore


store = KVStore()


@click.group()
def cli() -> None:
    """Run key-value store commands."""


@cli.command()
@click.argument("key")
@click.argument("value")
@click.argument("ttl", required=False, type=int, default=DEFAULT_TTL_SECONDS)
def set(key: str, value: str, ttl: int) -> None:
    store.set(key, value, ttl)
    click.echo(True)


@cli.command()
@click.argument("key")
def get(key: str) -> None:
    click.echo(store.get(key))


@cli.command()
@click.argument("key")
def delete(key: str) -> None:
    click.echo(store.delete(key))


@cli.command(name="list_keys")
def list_keys() -> None:
    for key in store.list_keys():
        click.echo(key)


if __name__ == "__main__":
    cli()
