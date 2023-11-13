import logging

from flask import Flask, render_template, request, jsonify

from constants import AppConstants
from interface import DBInterface, AppInterface
from model import db_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

appVersion = "v1"
baseUrl = f"/{appVersion}"
app = Flask(__name__)

db_interface = DBInterface(db_engine=db_engine)
app_interface = AppInterface(db_interface=db_interface)


# Helper methods
def _request_not_json_error():
    return jsonify({"result": "Request is expected to be a json"})


@app.route("/")
def index():
    return render_template("index.html")


@app.post(f"{baseUrl}/user/signup")
def user_signup():
    if not request.is_json:
        return _request_not_json_error()
    return jsonify(app_interface.user_signup(request=request.json))


@app.post(f"{baseUrl}/user/login")
def user_login():
    if not request.is_json:
        return _request_not_json_error()
    return jsonify(app_interface.user_login(request=request.json))


@app.post(f"{baseUrl}/user/<int:u_id>/logout")
def user_logout(u_id):
    auth_token = request.headers.get(AppConstants.authorization, "")
    return jsonify(app_interface.user_logout(u_id, auth_token))


@app.get(f"{baseUrl}/user/<int:u_id>/posts")
def get_user_posts(u_id):
    auth_token = request.headers.get(AppConstants.authorization, "")
    return jsonify(app_interface.get_user_posts(u_id, auth_token))


@app.post(f"{baseUrl}/posts/create")
def create_post():
    if not request.is_json:
        return _request_not_json_error()
    auth_token = request.headers.get(AppConstants.authorization, "")
    return jsonify(app_interface.create_post(auth_token, request.json))


if __name__ == "__main__":
    app.run(debug=True)
