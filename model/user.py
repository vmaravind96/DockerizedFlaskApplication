from sqlalchemy import String, Integer, Column

from constants import AppConstants
from model import DBBase


class User(DBBase):
    """
    Class for Posts
    """
    __tablename__ = "user"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(30))
    username = Column('username', String(30), nullable=False)
    password = Column('password', String(30), nullable=False)

    def to_dict(self):
        return {AppConstants.id: self.id, AppConstants.name: self.name, AppConstants.username: self.username,
                AppConstants.password: self.password}
