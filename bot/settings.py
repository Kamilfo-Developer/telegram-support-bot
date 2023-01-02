from typing import Type
from bot.db.repositories.repository import Repo
from bot.db.repositories.sa_repository import SARepo
from dotenv import load_dotenv
from pathlib import Path
import os

# Path to .env file where the bot token is stored
DOTENV_PATH: Path | str = Path("../.env")

load_dotenv(DOTENV_PATH)


# Repository that will be used for getting access to the DB
# Defaults to SARepo, which implemented using SQLAlchemy
RepositoryClass: Type[Repo] = SARepo

# Language code that satisfies IETF standard
# (https://en.wikipedia.org/wiki/IETF_language_tag)
DEFAULT_LANGUAGE_CODE: str = "en"

BOT_TOKEN = os.getenv("BOT_TOKEN")
