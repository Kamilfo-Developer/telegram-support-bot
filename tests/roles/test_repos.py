import pytest

from app.roles.entities import Role
from app.roles.repo import RolesRepo
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.value_objects import RolePermissions
from app.support_users.repo import SupportUsersRepo


# TODO: Write tests for getting


@pytest.mark.asyncio
async def test_getting_roles(
    fill_db,
    roles_repo: RolesRepo,
):
    all_roles = await roles_repo.get_all()

    assert await roles_repo.get_by_id(all_roles[0]._id) in all_roles

    assert await roles_repo.get_by_name(all_roles[0].name) in all_roles


@pytest.mark.asyncio
async def test_adding_roles(
    fill_db,
    roles_repo: RolesRepo,
):
    role = Role.create(
        RoleName("Senior support specialist"),
        RoleDescription("Answers VIP-clients questions and can assign roles"),
        RolePermissions(
            True,
            True,
        ),
    )

    await roles_repo.add(role)

    assert role == await roles_repo.get_by_id(role._id)
    assert role in await roles_repo.get_all()


@pytest.mark.asyncio
async def test_updating_roles(
    fill_db,
    roles_repo: RolesRepo,
    support_users_repo: SupportUsersRepo,
):
    role = (await roles_repo.get_all())[0]

    new_desrtiption = RoleDescription("A new description")

    new_name = RoleName("A new role name")

    new_permissions = RolePermissions(
        not role.permissions.can_answer_questions,
        role.permissions.can_manage_support_users,
    )

    role.description = new_desrtiption

    role.name = new_name

    role.permissions = new_permissions

    await roles_repo.update(role)

    updated_role = await roles_repo.get_by_id(role._id)

    assert updated_role is not None
    assert updated_role.description == new_desrtiption
    assert updated_role.name == new_name
    assert updated_role.permissions == new_permissions

    for support_user in await support_users_repo.get_by_role_id(role._id):
        assert (
            support_user.role
            and support_user.role.permissions == new_permissions
        )


@pytest.mark.asyncio
async def test_deleting_all_roles(
    fill_db,
    roles_repo: RolesRepo,
    support_users_repo: SupportUsersRepo,
):
    await roles_repo.delete_all()

    all_sup_users = await support_users_repo.get_all()

    assert all_sup_users != []

    for sup_user in all_sup_users:
        assert sup_user.role == None


@pytest.mark.asyncio
async def test_deleting_roles_by_id(
    fill_db,
    roles_repo: RolesRepo,
    support_users_repo: SupportUsersRepo,
):
    role = (await roles_repo.get_all())[0]

    await roles_repo.delete(role._id)

    assert (await roles_repo.get_by_id(role._id)) == None

    for support_user in await support_users_repo.get_all():
        assert support_user.role is None or support_user.role._id != role._id
