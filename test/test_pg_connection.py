import pytest

from src.util.pg_connection import connect_to_db, close_connection


def test_connect_to_db_connects():
    assert connect_to_db()


def test_connect_to_db_fails_with_wrong_details(monkeypatch):
    monkeypatch.setenv("PG_USER", "error")
    db = None
    try:
        with pytest.raises(Exception):
            db = connect_to_db()
    finally:
        if db:
            close_connection(db)


def test_close_connection():
    db = connect_to_db()
    result = db.run("SELECT * FROM STAFF")
    assert isinstance(result, list)
    close_connection(db)
    with pytest.raises(Exception):
        db.run("SELECT * FROM STAFF")
