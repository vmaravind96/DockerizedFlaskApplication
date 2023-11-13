from sqlalchemy import Integer, Column, Text, ForeignKey

from model import DBBase


class Login(DBBase):
    """
    Class for Login
    """
    __tablename__ = "login"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    token = Column('token', Text, nullable=False)
