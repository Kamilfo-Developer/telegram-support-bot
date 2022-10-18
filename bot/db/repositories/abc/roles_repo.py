from typing import Iterable
from uuid import UUID
import abc


class RolesRepo(abc.ABC):
    @abc.abstractmethod
    def get_all_roles(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_all_roles(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete_role(self, role_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def get_role(self, role_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def add_role(self, role):
        raise NotImplementedError
