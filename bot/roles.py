import abc


class SupportRole(abc.ABC):
    can_answer_questions: bool
    is_like_root: bool
    can_create_roles: bool
    can_romove_roles: bool
    can_change_roles: bool
    can_assign_role: bool
