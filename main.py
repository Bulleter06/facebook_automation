import os
from dotenv import load_dotenv
from browser import Browser

if __name__ == "__main__":
    load_dotenv()

    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    Browser(login=login, password=password)
