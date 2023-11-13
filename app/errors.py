class PermissionDeniedError(Exception):
    pass


class UserIsNotAuthorizedError(Exception):
    pass


class NoSuchEntityError(Exception):
    pass


class AnswerAlreadyEstimatedError(Exception):
    pass


class NoLastQuestionError(Exception):
    pass


class NoSuchSupportUser(Exception):
    pass


class RoleNameDuplicationError(Exception):
    pass


class NoSuchRole(Exception):
    pass


class NoSuchRegularUser(Exception):
    pass


class NoSuchQuestion(Exception):
    pass


class SupportUserAlreadyExists(Exception):
    pass


class IncorrectActionError(Exception):
    pass


class NoBoundQuestion(Exception):
    pass


class NoSuchAnswer(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass


class OwnerAlreadyInitialized(Exception):
    pass


class IncorrectCallbackDataError(Exception):
    pass


class IncorrectRepoTypeProvided(Exception):
    pass


class IncorrectDBConfigTypeProvided(Exception):
    """Exception raised if incorrect db_config provided

    Attributes:
        message - explanation of the error
    """

    def __init__(
        self,
    ):
        super().__init__(
            "db_config must be an instance of next classes: SADBConfig"
        )


class IncorrectOwnerDefaultDescriptiveNameProvided(Exception):
    """Exception raised if the provided sting
    doesn't satisfy DescriptiveName's constraints

    Attributes:
        message - explanation of the error
    """

    def __init__(self, allowed_name_length: int):
        super().__init__(
            f"OWNER_DEFAULT_DESCRIPTIVE_NAME parameter's length "
            f"should be less or equal to {allowed_name_length}"
        )


class SameValueAssigningError(Exception):
    pass


class EntityAlreadyExists(Exception):
    pass


class NoBotTokenProvided(Exception):
    pass
