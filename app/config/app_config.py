from enum import Enum
import os

import pytz
from pytz import BaseTzInfo
from tzlocal import get_localzone

from pydantic import BaseSettings, validator
from app.errors import IncorrectOwnerDefaultDescriptiveNameProvided

from app.support_users.value_objects import DescriptiveName


class RepoType(str, Enum):
    SA = "SA"


class SADBProviderType(str, Enum):
    SQLITE = "SQLITE"
    POSTGRES = "POSTGRES"
    MYSQL = "MYSQL"


class AppSettings(BaseSettings):
    # Needed for some developing features
    # Should be False in production
    DEBUG = os.getenv("DEBUG") or False

    # Should be a member of tz database
    # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
    TIMEZONE: str | BaseTzInfo | None

    @validator("TIMEZONE")
    def get_timezone(cls, v):
        timezone = v and pytz.timezone(v) or get_localzone()

        return timezone

    # Repository that will be used for getting access to the DB
    # Defaults to 'SA', which is implemented using SQLAlchemy
    REPO_TYPE: RepoType = RepoType.SA

    # DB Provider for SQLAlchemy
    SA_DB_PROVIDER: SADBProviderType = SADBProviderType.SQLITE

    # Language code that satisfies IETF standard
    # (https://en.wikipedia.org/wiki/IETF_language_tag)
    DEFAULT_LANGUAGE_CODE: str = "en"

    @validator("DEFAULT_LANGUAGE_CODE")
    def lowercase_language_code(cls, v: str):
        return v.lower()

    # Your bot token, can be taken from here:
    # https://t.me/botfather
    BOT_TOKEN: str

    OWNER_PASSWORD: str

    OWNER_DEFAULT_DESCRIPTIVE_NAME: str | DescriptiveName = "Owner"

    @validator("OWNER_DEFAULT_DESCRIPTIVE_NAME")
    def validate_owner_defaul_descriptive_name(cls, v: str) -> DescriptiveName:
        try:
            return DescriptiveName(v)
        except ValueError:
            raise IncorrectOwnerDefaultDescriptiveNameProvided(
                DescriptiveName.MAX_LENGTH
            )

    class Config:
        env_file = ".env"
