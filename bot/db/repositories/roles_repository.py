from bot.roles import Role
from uuid import UUID
import abc


class RolesRepository(abc.ABC):
    def get_all_roles():
        raise NotImplementedError

    def delete_all_roles():
        raise NotImplementedError

    def delete_role(role_id: UUID):
        raise NotImplementedError

    def get_role(role_id: UUID):
        raise NotImplementedError

    def add_role(role: Role):
        raise NotImplementedError
