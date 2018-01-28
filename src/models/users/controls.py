from src.common import CONSTANTS
from src.common.database import Database
import src.models.users.errors as UserErrors
from src.common.utils import Utils
import uuid


class User(object):

    def __init__(self,email, password,user_name,first_name,last_name, _id=None):
        self.email = email
        self.password = password
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self._id = uuid.uuid4().hex if _id is None else _id


    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one("users", {"email": email})  # Password in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password, first_name, last_name, user_name):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one("users", {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.hash_password(password),first_name, last_name,user_name).save_to_db()

        return True

    @staticmethod
    def get_by_email(email):
         Database.initialize()
         return User(**Database.find_one("users", {"email": email}))

    @staticmethod
    def get_by_user_name(user_name):
        Database.initialize()
        return User(**Database.find_one("users", {"user_name": user_name}))


    def save_to_db(self):
        Database.update('users', {"_id": self._id}, self.json())

    def url(self):
        return CONSTANTS.url + r'users/' + self.user_name

    def __eq__(self, other):
        return self._id == other._id

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name
        }

    def __repr__(self):
        return "{} {}".format(self.first_name.capitalize(), self.last_name.capitalize())

if __name__ == "__main__":
    pass
