import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        # Determine the environment
        self.ENV = os.getenv("ENV", "development")

        # Load the appropriate .env file
        if self.ENV == "test":
            load_dotenv(".env.test")
        else:
            load_dotenv()  # This loads the default .env file

        # Database configuration
        self.DB_USERNAME = os.getenv("DB_USERNAME")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")

        # API Keys
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

        # Other configurations
        self.API_KEY = os.getenv("API_KEY")

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def IS_TESTING(self):
        return self.ENV == "test"


# Create a global instance of the Config class
config = Config()
