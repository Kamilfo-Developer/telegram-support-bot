from app.utils import StrWithMaxLength


class RoleName(StrWithMaxLength):
    MAX_LENGTH = 256


class RoleDescription(StrWithMaxLength):
    MAX_LENGTH = 4096
