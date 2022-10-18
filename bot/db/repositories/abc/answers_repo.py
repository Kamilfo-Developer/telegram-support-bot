from uuid import UUID
import abc


class AnswersRepo(abc.ABC):
    @abc.abstractmethod
    async def get_all_answers(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_by_id(self, answer_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_answers_with_question_id(self, question_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_answer_with_id(self, answer_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_answers(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_answers_with_question_id(self, question_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_answer_to_question(
        self,
        answer,
        question,
        support_user,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def count_all_answers(self) -> int:
        raise NotImplementedError
