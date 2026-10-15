"""Apply pending database migrations using Alembic.

For a database created before Alembic was introduced, verify that its schema
matches the initial migration and run ``alembic stamp head`` once before using
this script. Stamping records the current schema version without changing data.
"""

from alembic import command
from alembic.config import Config


def main() -> None:
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")


if __name__ == "__main__":
    main()
