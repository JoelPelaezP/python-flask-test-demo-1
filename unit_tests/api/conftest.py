import os
import sys

from sqlalchemy import text

# insert root directory into python module search path
sys.path.insert(1, os.getcwd())
import uuid

import pytest
from sqlalchemy.orm import sessionmaker

import app
import database.config.db as db
from database.models.base import Base


def db_test_create_schema(db_config):
    sql_create_schema = f"CREATE SCHEMA IF NOT EXISTS {db_config.schema_name} AUTHORIZATION {db_config.user}"

    db_engine = db.get_db_engine(db_config)
    with db_engine.begin() as connection:
        connection.execute(text(sql_create_schema))

    print(f"INFO: Created schema {db_config.schema_name}")


def db_test_drop_schema(db_config):
    sql_drop_schema = f"DROP SCHEMA {db_config.schema_name} CASCADE"

    db_engine = db.get_db_engine(db_config)
    with db_engine.begin() as connection:
        connection.execute(text(sql_drop_schema))

    print(f"INFO: Dropped schema {db_config.schema_name} ")


@pytest.fixture(scope="session")
def db_test_schema(db_config):
    db_test_create_schema(db_config)

    yield db_config

    db_test_drop_schema(db_config)


@pytest.fixture(scope="session")
def db_test(db_test_schema):
    db_engine = db.get_db_engine(db_test_schema)
    Base.metadata.create_all(bind=db_engine)
    db_session = db.db_start(db_test_schema)
    db_session.close()

    return db_engine


@pytest.fixture(scope="session")
def db_session_maker(db_test):
    return sessionmaker(autocommit=False, expire_on_commit=False)


@pytest.fixture(scope="session")
def test_db_session(db_test, db_session_maker):
    c = db_test.connect()
    t = c.begin()
    s = db_session_maker(bind=c, join_transaction_mode="create_savepoint")

    yield s

    s.close()
    t.rollback()
    c.close()


@pytest.fixture(scope="session")
def init_factory_session(test_db_session):
    import database.models.factories as db_factory

    db_factory.db_session = test_db_session


@pytest.fixture(scope="session")
def db_config():
    return db.DBConfig(
        user="postgres",
        password="Chr0me#1",
        dbname="flask_test_dev",
        schema_name=f"api_db_test_schema_{uuid.uuid4().int}",
    )


@pytest.fixture(scope="session")
def flask_app(init_factory_session, db_config):
    return app.create_app(db_config, True)


@pytest.fixture
def test_app_client(flask_app):
    return flask_app.test_client()
