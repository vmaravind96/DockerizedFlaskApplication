import uuid

from constants import AppConstants
from interface import DBInterface


class AppInterface:

    def __init__(self, db_interface: DBInterface):
        self.db_interface = db_interface

    def user_signup(self, request):
        name = request.get(AppConstants.name, "")
        username = request.get(AppConstants.username, None)
        password = request.get(AppConstants.password, None)

        if username is None or password is None:
            return {AppConstants.error: "Username / password not provided"}
        old_user = self.db_interface.query_user(username=username)
        if old_user:
            return {AppConstants.error: "Username already exists"}
        isSuccess = self.db_interface.create_user(name, username, password)
        if not isSuccess:
            return {AppConstants.error: "User creation failed"}
        user = self.db_interface.query_user(username=username)
        return user.to_dict()

    def user_login(self, request):
        username = request.get(AppConstants.username, None)
        password = request.get(AppConstants.password, None)

        if username is None or password is None:
            return {AppConstants.error: "Username / password not provided"}
        user = self.db_interface.query_user(username=username)
        if user.password != password:
            return {AppConstants.error: "Invalid credentials"}

        token = self.generate_uuid()
        isLoginSuccess = self.db_interface.create_login(user_id=user.id, token=token)
        if not isLoginSuccess:
            return {AppConstants.error: "Unable to login at the moment"}

        return {AppConstants.id: user.id, AppConstants.token: token}

    def user_logout(self, u_id, token):
        login = self.db_interface.query_login(user_id=u_id, token=token)
        if login is None:
            return {AppConstants.error: "User not logged in inorder to logout"}
        is_success = self.db_interface.delete_login(login)
        if not is_success:
            return {AppConstants.error: "Unable to logout at the moment"}
        return {AppConstants.success: "Logout successful"}

    def get_user_posts(self, u_id, token):
        is_logged_in, user = self.is_logged_in(u_id, token)
        if not is_logged_in:
            return {AppConstants.error: "User not logged in. Please login first"}
        posts = self.db_interface.query_posts_for_user(u_id)
        return {AppConstants.posts: [p.to_dict() for p in posts]}

    def create_post(self, token, request):
        user_id = request.get(AppConstants.user_id, None)
        if user_id is None:
            return {AppConstants.error: "User id missing in request"}
        is_logged_in, user = self.is_logged_in(user_id, token)
        if not is_logged_in:
            return {AppConstants.error: "User not logged in. Please login first"}

        title = request.get(AppConstants.title, None)
        content = request.get(AppConstants.content, None)

        if title is None or content is None:
            return {AppConstants.error: "Title / content is missing for the post"}
        is_success = self.db_interface.create_post(title=title, content=content, user_id=user_id)
        if not is_success:
            return {AppConstants.error: "Post creation failed"}
        return {AppConstants.success: "Post creation successful"}

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    def is_logged_in(self, user_id, token):
        login = self.db_interface.query_login(user_id=user_id, token=token)
        if login is None:
            return False, None
        user = self.db_interface.query_user_with_id(user_id=user_id)
        return True, user
