import sqlite3
import datetime
import bcrypt
import base64, hashlib

from server.users import User

CONNECTION_STRING = "datastore/therecipehub.db"


def create_user(user, connection_string):
    hashed_password = hashlib.sha256(user.password.encode("utf-8")).digest()
    hashed_password = base64.b64encode(hashed_password)
    hashed_password = bcrypt.hashpw(hashed_password, bcrypt.gensalt())
    hashed_password = hashed_password.decode("utf-8")
    user.password = hashed_password

    user.created_at = datetime.datetime.now().strftime("%D %H:%M")
    user.updated_at = user.created_at

    user_dict = user.to_dict()
    user_dict.pop("second_password", None)

    query = "INSERT INTO users ({}) VALUES ({})".format(
        ", ".join(user_dict.keys()),
        ", ".join("?" * len(user_dict))
    )
    print(query)
    conn = sqlite3.connect(connection_string)
    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(user_dict.values()))
        print(tuple(user_dict.values()))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def get_user_by_email(user, connection_string):
    conn = sqlite3.connect(connection_string)
    # create select query
    query = f"select id, username, fullname, email, password from users where email = '{user.email}';"

    # initialise a cursor
    cursor = conn.cursor()

    # execute query using the cursor
    results = cursor.execute(query).fetchone()

    cursor.close()
    conn.close()

    current_user = User.from_list(results)
    return current_user

def search_for_email(user, connection_string):
    conn = sqlite3.connect(connection_string)

    # create select query
    query = f"select email from users where email = '{user.email}';"

    # initialise a cursor
    cursor = conn.cursor()

    # execute query using the cursor
    results = cursor.execute(query).fetchone()

    cursor.close()
    conn.close()

    if results == None:
        return True
    return False

def get_all_users(connection_string):
    conn = sqlite3.connect(connection_string)
    query = "select id, username, fullname, email, password from users"
    cursor = conn.cursor()
    results = cursor.execute(query).fetchall()
    cursor.close()
    conn.close()
    users = []
    for user in results:
        current_user = User.from_list(user)
        users.append(current_user)
    return users


def edit_user_by_email(user, connection_string):
    user_dict = user.to_dict()
    query = "UPDATE users SET "
    for key, value in user_dict.items():
        if isinstance(value, str) and value is not None:
            query += f" {key} = ?,"
        elif value is not None:
            query += f" {key} = ?,"
    query = query[:-1] + " WHERE email = ?"
    try:
        conn = sqlite3.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(query, [value if isinstance(value, str) else str(value) for value in user_dict.values()] + [user.email])
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
# def edit_user_by_email(user, connection_string):
#     user_dict = user.to_dict()
#     query = "UPDATE users SET "
#     for key, value in user_dict.items():
#         if isinstance(value, str) and value is not None:
#             query += f" {key} = '{value}',"
#         elif value is not None:
#             query += f" {key} = {value},"
#     query = query[:-1] # get all characters up to last
#     query += f" WHERE email = '{user.email}';"
#     print(query)
#     conn = sqlite3.connect(connection_string)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(query)
#         conn.commit()
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         cursor.close()
#         conn.close()
#         raise e

def delete_user_by_email(user, connection_string):
    query = "DELETE FROM users "
    query += f" WHERE email = '{user.email}';"
    print(query)
    conn = sqlite3.connect(connection_string)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        cursor.close()
        conn.close()
        raise e