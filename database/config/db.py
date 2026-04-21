import psycopg2
import sqlalchemy.pool
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from contextlib import contextmanager
from typing import Any, cast
from utility.pydantic import PydanticBaseSettings

def db_start() -> Session:
    print("INFO: Initializing DB")

    def get_connection():
        connection = get_db_connection()
        return psycopg2.connect(**connection)
    
    db_pool = sqlalchemy.pool.QueuePool(get_connection, pool_size=3, max_overflow=2, timeout=5)
    db_engine = sqlalchemy.create_engine("postgresql://", pool=db_pool)
    db_engine.connect()

    print("INFO: Successfully connected to DB")

    session =  scoped_session(session_factory=sessionmaker(bind=db_engine, expire_on_commit=False, autocommit=False ))

    db_engine.dispose()

    return cast(Session, session)

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


def build_connection_uri():
    connection = get_db_connection()

    return f"postgresql://{connection['user']}:{connection['password']}@{connection['host']}:{connection['port']}/{connection['dbname']}"

class DBConfig(PydanticBaseSettings):
    user:str
    password:str
    host: str
    port:int
    dbname:str

    class Config:
        env_prefix = "DATABASE_"

def get_db_config()-> DBConfig:
    return DBConfig()

def get_db_connection()-> dict[str:Any]:
    db_config:DBConfig = get_db_config()
    connection = {
        "host" : db_config.host,
        "dbname":db_config.dbname,
        "user":db_config.user,
        "password":db_config.password,
        "port":db_config.port
    }
    return connection
