from contextlib import contextmanager
from typing import Any, cast

import psycopg2
import sqlalchemy.pool
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from utility.pydantic import PydanticBaseSettings


class DBConfig(PydanticBaseSettings):
    user: str
    password: str
    host: str
    port: int
    dbname: str
    schema_name: str

    class Config:
        env_prefix = "DATABASE_"


def get_db_config() -> DBConfig:
    return DBConfig()


def db_start(db_config: DBConfig = None) -> Session:
    print("INFO: Initializing DB")

    db_engine = get_db_engine(db_config)
    db_engine.connect()

    print("INFO: Successfully connected to DB")

    session = scoped_session(
        session_factory=sessionmaker(
            bind=db_engine, expire_on_commit=False, autocommit=False
        )
    )

    db_engine.dispose()

    return cast(Session, session)


def get_db_engine(db_config: DBConfig = None):
    db_config = db_config if db_config is not None else get_db_config()

    def get_connection():
        connection = get_db_connection(db_config)
        return psycopg2.connect(**connection)

    db_pool = sqlalchemy.pool.QueuePool(
        get_connection, pool_size=3, max_overflow=2, timeout=5
    )
    db_engine = sqlalchemy.create_engine("postgresql://", pool=db_pool)

    return db_engine


@contextmanager
def get_scoped_session(session: Session):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def build_connection_url(db_config: DBConfig):
    connection = get_db_connection(db_config)

    return f"postgresql://{connection['user']}:{connection['password']}@{connection['host']}:{connection['port']}/{connection['dbname']}"


def get_db_connection(db_config: DBConfig) -> dict[str:Any]:
    connection = {
        "host": db_config.host,
        "dbname": db_config.dbname,
        "user": db_config.user,
        "password": db_config.password,
        "port": db_config.port,
        "options": f"-c search_path={db_config.schema_name}",
    }
    return connection
