from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from app.errors import IncorrectDBConfigTypeProvided

from app.roles.controller import RolesController
from app.roles.infra.sa_repo import SARolesRepo
from app.roles.repo import RolesRepo
from app.shared.db import DBConfig, SADBConfig


def get_roles_repo(
    db_config: DBConfig,
) -> RolesRepo:
    if isinstance(db_config, SADBConfig):
        return SARolesRepo(db_config)

    raise IncorrectDBConfigTypeProvided()


class RolesContainer(DeclarativeContainer):
    db_config = Dependency(DBConfig)  # type: ignore

    roles_repo = Singleton(get_roles_repo, db_config)

    roles_controller = Singleton(
        RolesController,
        roles_repo=roles_repo,
    )
