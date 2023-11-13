import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from model import User, Login, Posts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DBInterface:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def create_user(self, name, username, password):
        user = User(name=name, username=username, password=password)
        with Session(self.db_engine) as sess:
            try:
                sess.add(user)
            except Exception as ex:
                sess.rollback()
                logger.error(f"Error adding user: {str(ex)}")
                return False
            else:
                sess.commit()
        return True

    def query_user(self, username):
        with Session(self.db_engine) as sess:
            stmt = select(User).where(User.username == username)
            user = sess.scalars(stmt).first()
        return user

    def query_user_with_id(self, user_id):
        with Session(self.db_engine) as sess:
            stmt = select(User).where(User.id == user_id)
            user = sess.scalars(stmt).first()
        return user

    def create_login(self, user_id, token):
        login = Login(user_id=user_id, token=token)
        with Session(self.db_engine) as sess:
            try:
                sess.add(login)
            except Exception as ex:
                sess.rollback()
                logger.error(f"Error adding login entry: {str(ex)}")
                return False
            else:
                sess.commit()
        return True

    def query_login(self, user_id, token):
        with Session(self.db_engine) as sess:
            stmt = select(Login).where(Login.user_id == user_id, Login.token == token)
            login = sess.scalars(stmt).first()
        return login

    def delete_login(self, login):
        with Session(self.db_engine) as sess:
            try:
                sess.delete(login)
            except Exception as ex:
                sess.rollback()
                logger.error(f"Error deleting login entry: {str(ex)}")
                return False
            else:
                sess.commit()
        return True

    def query_posts_for_user(self, user_id):
        with Session(self.db_engine) as sess:
            stmt = select(Posts).where(Posts.user_id == user_id)
            posts = sess.scalars(stmt).all()
        return posts

    def create_post(self, title, content, user_id):
        post = Posts(title=title, content=content, user_id=user_id)
        with Session(self.db_engine) as sess:
            try:
                sess.add(post)
            except Exception as ex:
                sess.rollback()
                logger.error(f"Error creating post: {str(ex)}")
                return False
            else:
                sess.commit()
        return True
