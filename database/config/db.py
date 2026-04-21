import psycopg2
import sqlalchemy.pool
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from contextlib import contextmanager
from typing import cast

def db_start() -> Session:
    print("INFO: Initializing DB")

    def get_connection():
        connection = {
            "host" : "python-flask-db",
            "dbname":"flask_test_dev",
            "user":"postgres",
            "password":"Chr0me#1",
            "port":"5432"
        }
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
    connection = {
        "host" : "localhost",
        "dbname":"flask_test_dev",
        "user":"postgres",
        "password":"Chr0me#1",
        "port":"5432"
    }

    return f"postgresql://{connection['user']}:{connection['password']}@{connection['host']}:{connection['port']}/{connection['dbname']}"