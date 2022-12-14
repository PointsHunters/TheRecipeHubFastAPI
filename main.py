import datetime
import json

from fastapi import FastAPI
from pydantic import BaseModel

from server.register import signup, signin
from server.repository import CONNECTION_STRING, get_all_users, edit_user_by_email
from server.users import User

app = FastAPI()

class Item(BaseModel):
    id: int | None = None
    name: str
    email: str
    password: str
    second_password: str
    created_at: str | None = None
    updated_at: str | None = None

@app.get("/")
def welcome():
    return "<h1>Welcome to TheRecipeHub's API</h1>", 200

@app.get("/api/v1/version")
def version():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    response = {
        "name": "therecipehub-api",
        "version": "v0.0.1",
        "last_updated": "2022-12-14T17:48:00",
        "request_time": now
    }
    response = json.dumps(response)
    return response, 200

@app.post("/api/v1/register")
def register(request: Item):
    try:
        request_body = request.dict()
        print(request_body)
        signup(request_body, CONNECTION_STRING)
        return "", 204
    except Exception as e:
        error_message = {
            "error": f"Failed to create user. Cause: {e}."
        }
        error_json = json.dumps(error_message)
        return error_json, 500

@app.post("/api/v1/authenticate")
def authenticate(request: Item):
    try:
        request_body = request.json
        user = signin(request_body, CONNECTION_STRING)
        return user.to_json(), 200
    except Exception as e:
        error_message = {
            "error": f"Failed to authenticate user. Cause: {e}."
        }
        error_json = json.dumps(error_message)
        return error_json, 500

@app.api_route("/api/v1/users", methods=["GET", "PUT", "DELETE"]) # put delete
def users(request: Item):
    if request.method == "GET":
        try:
            users = get_all_users(CONNECTION_STRING)
            response = [user.to_dict() for user in users]
            response = json.dumps(response)
            return response, 200
        except Exception as e:
            error_message = {
                "error": f"Failed to get all users. Cause: {e}."
            }
            error_json = json.dumps(error_message)
            return error_json, 500

    if request.method == "PUT":
        request_body = request.json
        if request_body.get("email") is None:
            error_message = {
                "error": f"Failed to update user. Missing user email."
            }
            error_json = json.dumps(error_message)
            return error_json, 500

        user = User.from_dict(request_body)
        edit_user_by_email(user, CONNECTION_STRING)
        return "", 204

    if request.method == "DELETE":
        pass