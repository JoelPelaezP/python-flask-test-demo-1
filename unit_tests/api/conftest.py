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


def test_db_create_schema(test_db_config):
    sql = f"CREATE SCHEMA IF NOT EXISTS {test_db_config.schema_name} AUTHORIZATION {test_db_config.user}"

    db_engine = db.get_db_engine(test_db_config)
    with db_engine.begin() as connection:
        connection.execute(text(sql))


def test_db_drop_schema(test_db_config):
    sql = f"DROP SCHEMA {test_db_config.schema_name} CASCADE"

    db_engine = db.get_db_engine(test_db_config)
    with db_engine.begin() as connection:
        connection.execute(text(sql))


@pytest.fixture(scope="session")
def test_db_schema(test_db_config):
    test_db_create_schema(test_db_config)

    yield test_db_config

    test_db_drop_schema(test_db_config)


@pytest.fixture(scope="session")
def test_db_engine(test_db_schema):
    db_engine = db.get_db_engine(test_db_schema)
    Base.metadata.create_all(bind=db_engine)
    db_session = db.get_db_session(test_db_schema)
    db_session.close()

    return db_engine


@pytest.fixture(scope="session")
def test_db_session_maker(test_db_engine):
    return sessionmaker(autocommit=False, expire_on_commit=False)


@pytest.fixture(scope="session")
def test_db_session(test_db_engine, test_db_session_maker):
    c = test_db_engine.connect()
    t = c.begin()
    s = test_db_session_maker(bind=c, join_transaction_mode="create_savepoint")

    yield s

    s.close()
    t.rollback()
    c.close()


@pytest.fixture(scope="session")
def test_init_factory_session(test_db_session):
    import database.models.factories as db_factory

    db_factory.db_session = test_db_session


@pytest.fixture(scope="session")
def test_db_config():
    return db.DBConfig(
        user="postgres",
        password="Chr0me#1",
        dbname="flask_test_dev",
        schema_name=f"api_test_db_schema_{uuid.uuid4().int}",
    )


@pytest.fixture(scope="session")
def test_flask_app(test_init_factory_session, test_db_config):
    return app.create_app(test_db_config, True)


@pytest.fixture
def test_app_client(test_flask_app):
    return test_flask_app.test_client()
