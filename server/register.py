from server.repository import create_user, get_user_by_email
from server.users import User

import bcrypt
import base64, hashlib


def signup(request_body, connection_string):
    user = User.from_dict(request_body)

    user.username = user.validate_username()
    user.fullname = user.validate_fullname()
    user.email = user.validate_email()
    user.password = user.validate_password()

    if user.password != user.second_password:
        raise ValueError("Password mismatch. Try again using the same password.")

    create_user(user, connection_string)

def signin(request_body, connection_string):
    user = User.from_dict(request_body)

    user.email = user.validate_email()
    user_password = user.validate_password()

    existing_user = get_user_by_email(user, connection_string)

    # if existing_user is None:
    #     raise ValueError("No user found with the provided email.")
    
    hashed_password = hashlib.sha256(user_password.encode("utf-8")).digest()
    hashed_password = base64.b64encode(hashed_password)

    if bcrypt.checkpw(hashed_password, existing_user.password.encode("utf-8")):
        raise ValueError("Password mismatch.")

    existing_user.password = None
    # existing_user.second_password = None

    return existing_user