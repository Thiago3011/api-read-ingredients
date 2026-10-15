"""Safely prepare the database before starting a deployed application.

- A fresh database gets the Alembic migrations applied.
- A database already managed by Alembic is upgraded normally.
- A legacy database with the exact, verified pre-Alembic schema is stamped
  at the initial revision without modifying application data.
- An unexpected/unrecognized schema fails closed and requires manual review.
"""
from alembic import command
from alembic.config import Config
from sqlalchemy import Integer, String, inspect

from app.database import engine


EXPECTED_COLUMNS = {
    "users": {
        "id": (Integer, None),
        "name": (String, 100),
        "email": (String, 255),
        "password_hash": (String, 255),
    },
    "allergies": {
        "id": (Integer, None),
        "name": (String, 255),
        "user_id": (Integer, None),
    },
}


def schema_matches_initial_migration(database_inspector) -> bool:
    """Return True only when the legacy schema exactly matches revision head."""
    if set(database_inspector.get_table_names()) != {"users", "allergies"}:
        return False

    for table_name, expected_columns in EXPECTED_COLUMNS.items():
        reflected_columns = {
            column["name"]: column
            for column in database_inspector.get_columns(table_name)
        }
        if set(reflected_columns) != set(expected_columns):
            return False

        for column_name, (expected_type, expected_length) in expected_columns.items():
            column = reflected_columns[column_name]
            actual_type = column["type"]

            if not isinstance(actual_type, expected_type) or column["nullable"]:
                return False

            if expected_length is not None and actual_type.length != expected_length:
                return False

        primary_key = database_inspector.get_pk_constraint(table_name)
        if primary_key.get("constrained_columns") != ["id"]:
            return False

    user_email_index_found = any(
        index.get("unique") is True and index.get("column_names") == ["email"]
        for index in database_inspector.get_indexes("users")
    )
    allergy_user_index_found = any(
        index.get("column_names") == ["user_id"]
        for index in database_inspector.get_indexes("allergies")
    )
    allergy_foreign_key_found = any(
        foreign_key.get("constrained_columns") == ["user_id"]
        and foreign_key.get("referred_table") == "users"
        and foreign_key.get("referred_columns") == ["id"]
        and str(foreign_key.get("options", {}).get("ondelete", "")).upper() == "CASCADE"
        for foreign_key in database_inspector.get_foreign_keys("allergies")
    )

    return (
        user_email_index_found
        and allergy_user_index_found
        and allergy_foreign_key_found
    )


def main() -> None:
    alembic_config = Config("alembic.ini")
    database_inspector = inspect(engine)
    tables = set(database_inspector.get_table_names())

    if "alembic_version" in tables:
        print("Alembic version found; applying pending migrations.")
        command.upgrade(alembic_config, "head")
        return

    if not tables:
        print("Empty database detected; applying initial migration.")
        command.upgrade(alembic_config, "head")
        return

    if schema_matches_initial_migration(database_inspector):
        print(
            "Verified legacy schema detected; recording the initial Alembic "
            "revision without recreating tables or changing application data."
        )
        command.stamp(alembic_config, "head")
        command.upgrade(alembic_config, "head")
        return

    raise RuntimeError(
        "Database contains tables without an Alembic revision and does not "
        "match the verified initial schema. Automatic migration was stopped "
        "to protect existing data; inspect the database and migrate it manually."
    )


if __name__ == "__main__":
    main()
