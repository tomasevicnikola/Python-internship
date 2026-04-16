import sqlite3
from pathlib import Path

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        db = sqlite3.connect(current_app.config["DATABASE_PATH"])
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON;")
        g.db = db
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema_path = Path(current_app.root_path) / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as f:
        db.executescript(f.read())

    seed_pizzas(db)
    db.commit()


def seed_pizzas(db):
    pizzas = [
        ("Margherita", 8.5, 1),
        ("Pepperoni", 10.0, 1),
        ("Capricciosa", 11.5, 1),
        ("Vegetarian", 9.5, 1),
    ]

    db.executemany(
        """
        INSERT INTO pizzas (name, price, is_available)
        VALUES (?, ?, ?)
        """,
        pizzas,
    )


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialized and seeded.")


def init_app(app):
    Path(app.config["INSTANCE_DIR"]).mkdir(parents=True, exist_ok=True)

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)