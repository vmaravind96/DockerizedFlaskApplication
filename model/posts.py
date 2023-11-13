from sqlalchemy import String, Integer, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from constants import AppConstants
from model import User, DBBase


class Posts(DBBase):
    """
    Class for Posts
    """
    __tablename__ = "posts"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String(30))
    content = Column('content', Text)
    user_id = Column('user_id', ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", backref="posts")

    def to_dict(self):
        return {AppConstants.id: self.id, AppConstants.title: self.title, AppConstants.content: self.content,
                AppConstants.user_id: self.user_id}