from sqlalchemy import create_engine

from .db_base import DBBase
from .user import User
from .posts import Posts
from .login import Login


db_engine = create_engine("postgresql+psycopg2://admin:admin12345@db:5432/testdb", echo=False)
DBBase.metadata.create_all(db_engine)


