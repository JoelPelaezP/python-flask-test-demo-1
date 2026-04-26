from typing import cast

import factory
from sqlalchemy.orm import Session, scoped_session

import database.config.db as db
from database.models.store import StoreModel

db_session: Session | None = None


def get_db_session() -> Session:
    global db_session

    if db_session is None:
        db_session = db.get_db_session()

    return db_session


session = cast(
    Session,
    scoped_session(lambda: get_db_session(), scopefunc=lambda: get_db_session()),
)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"


class StoreFactory(BaseFactory):
    class Meta:
        model = StoreModel

    id = 31
    name = "dummy store"
