from uuid import UUID
import abc


class QuestionsRepo(abc.ABC):
    @abc.abstractmethod
    async def get_all_questions(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_question_by_id(self, answer_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_questions_with_question_id(self, question_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_unbinded_questions(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_unanswered_questions(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_question_with_id(self, answer_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_questions(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_questions_with_question_id(self, question_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_question(self, question, regular_user):
        raise NotImplementedError

    @abc.abstractmethod
    async def count_all_questions(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError
