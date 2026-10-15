import pytest

from app.database import normalize_database_url


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "postgres://user:pass@host.example:5432/db",
            "postgresql+psycopg://user:pass@host.example:5432/db",
        ),
        (
            "postgresql://user:pass@host.example:5432/db",
            "postgresql+psycopg://user:pass@host.example:5432/db",
        ),
        (
            "postgresql+psycopg://user:pass@host.example:5432/db",
            "postgresql+psycopg://user:pass@host.example:5432/db",
        ),
        ("sqlite:///./test.db", "sqlite:///./test.db"),
    ],
)
def test_normalize_database_url(source, expected):
    assert normalize_database_url(source) == expected
