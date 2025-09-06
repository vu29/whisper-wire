import asyncio
from contextlib import asynccontextmanager

import typer

from server.core.database import sessionmanager
from server.users.services.user_service import create_user

app = typer.Typer()

@asynccontextmanager
async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


@app.command("echo")
def echo(message: str):
    """Echo a message to the console."""
    typer.echo(message)

@app.command("add-user")
def add_user(name: str, password: str):
    """Add a new user to the database."""

    async def _add_user():
        async with get_db_session() as db:
            user = await create_user(db, name, password)
        typer.echo(f"✅ User created : {user.username}")

    asyncio.run(_add_user())


if __name__ == "__main__":
    app()
