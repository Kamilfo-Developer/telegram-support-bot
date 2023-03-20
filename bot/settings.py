from dotenv import load_dotenv
from pathlib import Path
from tzlocal import get_localzone
import pytz
import os

# Should be one of tz database
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
TIMEZONE = (
    os.getenv("TIMEZONE")
    and pytz.timezone(os.getenv("TIMEZONE"))  # type: ignore
    or get_localzone()
)

# Needed for some developing features
# Should be False when production
DEBUG = os.getenv("DEBUG") or False

# Path to .env file where the bot token is stored
DOTENV_PATH: Path | str = Path(".env")


load_dotenv(dotenv_path=DOTENV_PATH)


# Repository that will be used for getting access to the DB
# Defaults to 'sa', which is implemented using SQLAlchemy
REPO_TYPE: str = "sa"

# Language code that satisfies IETF standard
# (https://en.wikipedia.org/wiki/IETF_language_tag)
DEFAULT_LANGUAGE_CODE: str = os.getenv("DEFAULT_LANGUAGE_CODE") or "en"

# Your bot token, can be taken from here:
# https://t.me/botfather
BOT_TOKEN = os.getenv("BOT_TOKEN")


OWNER_PASSWORD = os.getenv("OWNER_PASSWORD")

OWNER_DEFAULT_DESCRIPTIVE_NAME = (
    os.getenv("OWNER_DEFAULT_DESCRIPTIVE_NAME") or "Owner"
)
