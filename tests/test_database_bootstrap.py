from sqlalchemy import Integer, String

from scripts.prepare_database import schema_matches_initial_migration


class FakeInspector:
    def __init__(self, *, columns=None, tables=None, indexes=None, foreign_keys=None, primary_keys=None):
        self.tables = tables or {"users", "allergies"}
        self.columns = columns or {
            "users": [
                {"name": "id", "type": Integer(), "nullable": False},
                {"name": "name", "type": String(100), "nullable": False},
                {"name": "email", "type": String(255), "nullable": False},
                {"name": "password_hash", "type": String(255), "nullable": False},
            ],
            "allergies": [
                {"name": "id", "type": Integer(), "nullable": False},
                {"name": "name", "type": String(255), "nullable": False},
                {"name": "user_id", "type": Integer(), "nullable": False},
            ],
        }
        self.indexes = indexes or {
            "users": [{"name": "ix_users_email", "column_names": ["email"], "unique": True}],
            "allergies": [{"name": "ix_allergies_user_id", "column_names": ["user_id"], "unique": False}],
        }
        self.foreign_keys = foreign_keys or {
            "allergies": [{
                "constrained_columns": ["user_id"],
                "referred_table": "users",
                "referred_columns": ["id"],
                "options": {"ondelete": "CASCADE"},
            }]
        }
        self.primary_keys = primary_keys or {
            "users": {"constrained_columns": ["id"]},
            "allergies": {"constrained_columns": ["id"]},
        }

    def get_table_names(self):
        return sorted(self.tables)

    def get_columns(self, table_name):
        return self.columns[table_name]

    def get_indexes(self, table_name):
        return self.indexes[table_name]

    def get_foreign_keys(self, table_name):
        return self.foreign_keys.get(table_name, [])

    def get_pk_constraint(self, table_name):
        return self.primary_keys[table_name]


def test_schema_matches_known_legacy_schema():
    assert schema_matches_initial_migration(FakeInspector())


def test_legacy_schema_rejects_unexpected_tables():
    inspector = FakeInspector(tables={"users", "allergies", "unknown_table"})

    assert not schema_matches_initial_migration(inspector)


def test_legacy_schema_rejects_extra_columns():
    inspector = FakeInspector()
    inspector.columns["users"].append(
        {"name": "unexpected", "type": String(20), "nullable": True}
    )

    assert not schema_matches_initial_migration(inspector)


def test_legacy_schema_requires_cascade_foreign_key():
    inspector = FakeInspector()
    inspector.foreign_keys["allergies"][0]["options"]["ondelete"] = "RESTRICT"

    assert not schema_matches_initial_migration(inspector)
