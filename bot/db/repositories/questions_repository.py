import abc
from uuid import UUID


class QuestionsRepository(abc.ABC):
    @abc.abstractclassmethod
    def clear_all_questions():
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_question_by_id(question_id: UUID):
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete_question_with_id(question_id: UUID):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_all_questions():
        raise NotImplementedError
