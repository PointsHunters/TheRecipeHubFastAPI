# uvicorn main:app --reload
import datetime
import json

from fastapi import FastAPI, Request
from pydantic import BaseModel

from server.register import signup, signin
from server.repository import CONNECTION_STRING, get_all_users, edit_user_by_email, search_for_email, delete_user_by_email
from server.users import User

app = FastAPI()

# class UserRegister(BaseModel):
#     id: int | None = None
#     name: str | None = None
#     email: str | None = None
#     password: str | None = None
#     second_password: str | None = None
#     created_at: str | None = None
#     updated_at: str | None = None

@app.get("/")
async def welcome():
    return "<h1>Welcome to TheRecipeHub's API</h1>", 200

@app.get("/api/v1/version")
async def version():
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    response = {
        "name": "therecipehub-api",
        "version": "v0.0.1",
        "last_updated": "2022-12-14T17:48:00",
        "request_time": now
    }
    response = json.dumps(response)
    return response, 200

class UserRegister(BaseModel):
    username: str
    fullname: str
    email: str
    password: str
    second_password: str

@app.post("/api/v1/register")
async def register(dbmodel: UserRegister):
    try:
        request_body = dbmodel.dict()
        print(request_body)
        signup(request_body, CONNECTION_STRING)
        return "", 204
    except Exception as e:
        error_message = {
            "error": f"Failed to create user. Cause: {e}."
        }
        error_json = json.dumps(error_message)
        return error_json, 500

class UserAuthenticate(BaseModel):
    email: str
    password: str
    # second_password: str

@app.post("/api/v1/authenticate")
async def authenticate(dbmodel: UserAuthenticate):
    try:
        request_body = dbmodel.dict()
        user = await signin(request_body, CONNECTION_STRING)
        return user.to_json(), 200
    except Exception as e:
        error_message = {
            "error": f"Failed to authenticate user. Cause: {e}."
        }
        error_json = json.dumps(error_message)
        return error_json, 500

@app.get("/api/v1/users")
async def users(request: Request):
    if request.method == "GET":
        try:
            users = await get_all_users(CONNECTION_STRING)
            response = [user.to_dict() for user in users]
            response = json.dumps(response)
            return json.loads(response), 200 # response converted to json
        except Exception as e:
            error_message = {
                "error": f"Failed to get all users. Cause: {e}."
            }
            error_json = json.dumps(error_message)
            return error_json, 500

class UserUpdate(BaseModel):
    username: str | None = None
    fullname: str | None = None
    email: str
    password: str

@app.put("/api/v1/users")
async def users(dbmodel: UserUpdate, request: Request):
    request_body = dbmodel.dict()
    user = User.from_dict(request_body)
    current_email = request_body.get("email") 

    if current_email is None:
        error_message = {
            "error": f"Failed to update user. Missing user email."
        }
        error_json = json.dumps(error_message)
        return error_json, 500
    elif await search_for_email(user, CONNECTION_STRING):
        error_message = {
            "error": f"Failed to update user. User not found."
        }
        error_json = json.dumps(error_message)
        return error_json, 500

    await edit_user_by_email(user, CONNECTION_STRING)
    return "", 204

class UserDelete(BaseModel):
    email: str
    password: str

@app.delete("/api/v1/users")
def users(dbmodel: UserDelete, request: Request):
    request_body = dbmodel.dict()
    user = User.from_dict(request_body)
    current_email = request_body.get("email")

    if current_email is None:
        error_message = {
            "error": f"Failed to delete user. Missing user email."
        }
        error_json = json.dumps(error_message)
        return error_json, 500
    elif search_for_email(user, CONNECTION_STRING):
        error_message = {
            "error": f"Failed to delete user. User not found."
        }
        error_json = json.dumps(error_message)
        return error_json, 500
    elif signin(request_body, CONNECTION_STRING) is None:
        error_message = {
            "error": f"Failed to delete user. Cause: Password mismatch."
        }
        error_json = json.dumps(error_message)
        return error_json, 500
    delete_user_by_email(user, CONNECTION_STRING)
    return "", 204