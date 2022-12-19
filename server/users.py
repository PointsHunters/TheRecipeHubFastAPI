import json


class User:
    special_characters = ["*", "?", "!", "#", "&", "=", "(", ")", "_", "-"]

    def __init__(self, id=None, username=None, fullname=None, email=None, password=None, second_password=None):
        self.id = id
        self.username = username
        self.fullname = fullname
        self.email = email
        self.password = password
        self.second_password = second_password
        self.created_at = None
        self.updated_at = None
        # self.special_characters = ["*", "?", "!", "#", "&", "=", "(", ")", "_", "-"]

    def validate_username(self):
        # eliminate spaces
        present_spaces = self.username.find(" ")
        if present_spaces > -1:
            raise ValueError("Invalid username. Username contains spaces.")

        # validate length
        if len(self.username) < 3:
            raise ValueError("Invalid username. Username too short. Minimum 3 characters required.")

        # validate special characters
        present_special = 0
        # present_digits = 0
        # present_upper = 0
        for character in self.username:
            if character in self.special_characters:
                present_special += 1  # present_special_characters = present_special_characters + 1

            # if character.isdigit():
            #     present_digits += 1

            # if character.isupper():
            #     present_upper += 1

            if present_special:
                break
            # if present_special and present_digits and present_upper:
            #     break

        if present_special != 0:
            raise ValueError("Invalid username. Special characters are not allowed.")

        # if present_digits == 0:
        #     raise ValueError("Invalid password. Missing at least one digit.")

        # if present_upper == 0:
        #     raise ValueError("Invalid password. Missing at least one upper case letter.")
        
        return self.username

    def validate_fullname(self):
        # eliminate spaces
        # present_spaces = self.fullname.find(" ")
        # if present_spaces > -1:
        #     raise ValueError("Invalid fullname. Fullname contains spaces.")

        # validate length
        if len(self.fullname) < 3:
            raise ValueError("Invalid fullname. Fullname too short. Minimum 3 characters required.")

        # validate special characters
        present_special = 0
        present_digits = 0
        # present_upper = 0
        for character in self.fullname:
            if character in self.special_characters:
                present_special += 1  # present_special_characters = present_special_characters + 1

            if character.isdigit():
                present_digits += 1

            # if character.isupper():
            #     present_upper += 1

            if present_special and present_digits:
                break
            # if present_special and present_digits and present_upper:
            #     break

        if present_special != 0:
            raise ValueError("Invalid fullname. Special characters are not allowed.")

        if present_digits != 0:
            raise ValueError("Invalid fullname. Numbers are not allowed.")

        # if present_upper == 0:
        #     raise ValueError("Invalid password. Missing at least one upper case letter.")
        
        return self.fullname

    def validate_email(self):
        email = self.email.lower()
        email = email.replace(" ", "")

        email_parts = email.split("@")

        if len(email_parts) > 2:
            raise ValueError("Email is not formatted correctly. Please try again.")

        second_part = email_parts[1]

        email_ending = second_part.split(".")

        if len(email_ending) > 2:
            raise ValueError("Email is not formatted correctly. Please try again.")

        return email

    def validate_password(self):
        # eliminate spaces
        present_spaces = self.password.find(" ")
        if present_spaces > -1:
            raise ValueError("Invalid password. Password contains spaces.")

        # validate length
        if len(self.password) < 8:
            raise ValueError("Invalid password. Password too short. Minimum 8 characters required.")

        # validate special characters
        present_special = 0
        present_digits = 0
        present_upper = 0
        for character in self.password:
            if character in self.special_characters:
                present_special += 1  # present_special_characters = present_special_characters + 1

            if character.isdigit():
                present_digits += 1

            if character.isupper():
                present_upper += 1

            if present_special and present_digits and present_upper:
                break

        if present_special == 0:
            raise ValueError("Invalid password. Special characters are missing.")

        if present_digits == 0:
            raise ValueError("Invalid password. Missing at least one digit.")

        if present_upper == 0:
            raise ValueError("Invalid password. Missing at least one upper case letter.")

        return self.password

    @staticmethod
    def print_hello():
        print("Hello")

    @classmethod
    def from_dict(cls, user_dict):
        id = user_dict.get("id")
        username = user_dict.get("username")
        fullname = user_dict.get("fullname")
        email = user_dict.get("email")
        password = user_dict.get("password")
        second_password = user_dict.get("second_password")
        created_at = user_dict.get("created_at")
        updated_at = user_dict.get("updated_at")

        obj = cls(id=id, username=username, fullname=fullname, email=email, password=password, second_password=second_password)
        obj.created_at = created_at
        obj.updated_at = updated_at
        return obj

    @classmethod
    def from_list(cls, user_list):
        if not user_list or user_list is None:
            raise ValueError("Invalid user details.")

        id = user_list[0]
        username = user_list[1]
        fullname = user_list[2]
        email = user_list[3]
        password = user_list[4]
        second_password = user_list[5]

        obj = cls(id=id, username=username, fullname=fullname, email=email, password=password, second_password=second_password)
        return obj

    def to_dict(self):
        user_dict = {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            "password": self.password,
            "second_password": self.second_password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        return user_dict

    def to_json(self):
        user_dict = self.to_dict()
        user_json = json.dumps(user_dict)
        return user_json