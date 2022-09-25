from uuid import UUID
import abc


class AnswersRepo(abc.ABC):
    @abc.abstractclassmethod
    def delete_all_answers(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_all_answers(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_answer_by_id(self, answer_id: UUID | int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete_answer_with_id(self, answer_id: UUID | int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_all_answers_with_question_id(self, question_id: UUID | int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def delete_all_answers_with_question_id(self, question_id: UUID | int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def count_all_answers(self) -> int:
        raise NotImplementedError
