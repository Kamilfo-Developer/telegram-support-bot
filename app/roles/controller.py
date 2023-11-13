from app.roles.entities import Role
from app.roles.repo import RolesRepo
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.value_objects import RoleIdType, RolePermissions


class RolesController:
    def __init__(self, roles_repo: RolesRepo) -> None:
        self.roles_repo = roles_repo

    async def delete_role(self, role_id: RoleIdType) -> None:
        await self.roles_repo.delete(role_id)

    async def add_role(
        self,
        role_name: str,
        role_description: str,
        can_answer_questions: bool,
        can_manage_support_user: bool,
    ) -> Role:
        role = Role.create(
            name=RoleName(role_name),
            description=RoleDescription(role_description),
            permissions=RolePermissions(
                can_answer_questions=can_answer_questions,
                can_manage_support_users=can_manage_support_user,
            ),
        )

        await self.roles_repo.add(role)

        return role

    async def get_role_by_name(self, name: str) -> Role | None:
        return await self.roles_repo.get_by_name(RoleName(name))

    async def get_all_roles(self) -> list[Role]:
        return await self.roles_repo.get_all()

    async def get_role(self, role_id: RoleIdType) -> Role | None:
        return await self.roles_repo.get_by_id(role_id)
