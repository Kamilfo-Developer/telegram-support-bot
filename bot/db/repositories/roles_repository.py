from uuid import UUID
import abc


class RolesRepository(abc.ABC):
    def get_all_roles(self):
        raise NotImplementedError

    def delete_all_roles(self):
        raise NotImplementedError

    def delete_role(self, role_id: UUID):
        raise NotImplementedError

    def get_role(self, role_id: UUID):
        raise NotImplementedError

    def add_role(self, role):
        raise NotImplementedError
