from typing import Type
from bot.db.repositories.repository import Repo
from bot.db.repositories.sa_repository import SARepo

# Repository that will be used for getting access to the DB
# Defaults to SARepo that implemented using SQLAlchemy
repository: Type[Repo] = SARepo

# Language code that satisfies IETF standard
# (https://en.wikipedia.org/wiki/IETF_language_tag)
default_language_code: str = "en"
