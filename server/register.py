from server.repository import create_user, get_user_by_email
from server.users import User


def signup(request_body, connection_string):
    user = User.from_dict(request_body)

    user.email = user.validate_email()
    user.password = user.validate_password()

    if user.password != user.second_password:
        raise ValueError("Password mismatch. Try again using the same password.")

    create_user(user, connection_string)


def signin(request_body, connection_string):
    user = User.from_dict(request_body)

    user.email = user.validate_email()
    user.password = user.validate_password()

    existing_user = get_user_by_email(user, connection_string)

    if user.password != existing_user.password:
        raise ValueError("Password mismatch.")

    existing_user.password = None
    existing_user.second_password = None

    return existing_user