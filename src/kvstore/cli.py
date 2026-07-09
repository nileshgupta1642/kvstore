import click

from .store import KVStore


store = KVStore()


@click.group()
def cli() -> None:
    """Run key-value store commands."""


@cli.command()
@click.argument("key")
@click.argument("value")
def set(key: str, value: str) -> None:
    store.set(key, value)
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
