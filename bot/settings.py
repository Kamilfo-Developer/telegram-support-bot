from typing import Type
from bot.db.repositories.repository import Repo
from bot.db.repositories.sa_repository import SARepo
from dotenv import load_dotenv
from pathlib import Path
import os

# Needed for some developing features
# Should be False when production
DEBUG = True

# Path to .env file where the bot token is stored
DOTENV_PATH: Path | str = Path(".env")


load_dotenv(dotenv_path=DOTENV_PATH)


# Repository that will be used for getting access to the DB
# Defaults to SARepo, which is implemented using SQLAlchemy
RepositoryClass: Type[Repo] = SARepo

# Language code that satisfies IETF standard
# (https://en.wikipedia.org/wiki/IETF_language_tag)
DEFAULT_LANGUAGE_CODE: str = "ru"

# Your bot token, can be taken from here:
# https://t.me/botfather
BOT_TOKEN = os.getenv("BOT_TOKEN")


OWNER_ID = int(os.getenv("OWNER_ID"))

OWNER_DEFAULT_DESCRIPTIVE_NAME = "Owner"
