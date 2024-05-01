import re
import firebase_admin

from datetime import datetime

from firebase_admin import db
from firebase_admin import credentials


class Uploader:
    def __init__(self):
        # Fetching the service account key JSON file
        cred = credentials.Certificate("serviceKey.json")
        # if not firebase_admin._apps:
        firebase_admin.initialize_app(
            cred, {"databaseURL": "https://auth-48749-default-rtdb.firebaseio.com/"}
        )

        # Saving the data
        ref = db.reference("auth/")
        self.users_ref = ref.child("users")

    # To upload data to the DB
    def upload(self, username, email, password):
        # Input validation
        if not isinstance(username, str):
            raise ValueError("Username must be a string")
        if not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        if not isinstance(password, str) or len(password) < 8:
            raise ValueError("Password must be a string with at least 8 characters")

        now = str(datetime.now()).split(".")[0].replace(" ", "--").replace(":", "-")
        self.users_ref.update(
            {
                username: {
                    "email": email,
                    "password": password,
                    "time_stamp": now,
                }
            }
        )

    # Read data from DB
    def get_data(self):
        print(self.users_ref.get())
        # print("Data Fetched Successfully!")
        return self.users_ref.get()

    # Delete ALL data from DB
    def delete_all(self):
        self.users_ref.delete()
        # print("Delete DB op, Successfully!")


if __name__ == "__main__":
    upl = Uploader()
    # # Entry 1
    # username = "aravind123"
    # email = "aravind@gmail.com"
    # password = "12345"

    # Entry 2
    username = "hrushi123"
    email = "hrushi@gmail.com"
    password = "456132123"

    # upl.upload(username, email, password)
    user_data = upl.get_data()
    # upl.delete_all()
    if "aravind" in user_data:
        print(user_data["aravind"]["password"])
    # print(user_data)
