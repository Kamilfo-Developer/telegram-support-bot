from mongo_db_config import MONGO_DB_NAME, MONGO_DB_URI_FOR_CLIENT, MONGO_DB_QUESTIONS_COLLECTION_NAME, MONGO_DB_ADMINS_COLLECTION_NAME, CERTIFICATE_PATH
from bson.objectid import ObjectId

import pymongo


class UserQuestions:
    def __init__(self, user_id: str) -> None:
        self.__user_id = user_id
    
    
    
    def get_random_unanswered_question():
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        data = list(collection.aggregate([
            {
                "$match": {
                    "answer_text": "",
                    "is_covered": False
                }
            },
            
            { 
                "$sample": {
                    "size": 1
                }
            }
        ]))
        
        return Question.from_data(data[0]) if data else None
    
    
    
    def get_questions_data(self):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        data = collection.find({"user_id": self.__user_id})

        if data:
            return list(data)
        
        return []
        
        
        
    def add_question(self, question_text: str, author: str = ""):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        collection.insert_one({
                "question_id": str(ObjectId()),
                "user_id": self.__user_id,
                "question_text": question_text,
                "author": author,
                "answer_text": "",
                "answer_author": "",
                "is_covered": False
            })
        
        
        
    def add_answer(self, question_id: str, answer_text: str, answer_author: str = ""):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        if collection.find_one({"user_id": self.__user_id, "question_id": question_id}):    
            collection.update_one({"user_id": self.__user_id, "question_id": question_id}, {
                    "$set":  {
                        "answer_text": answer_text, 
                        "answer_author": answer_author
                    }
                })

            return
    
        raise ValueError(f"No such question with this question_id ({question_id}) in questions of user with next user_id: {self.__user_id}")
    
    
    
    def delete_user_question(self, question_id: str):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        collection.delete_one({
            "user_id": self.__user_id,
            "question_id": question_id
        })
        
        
        
    def delete_question(question_id: str):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        collection.delete_one({
            "question_id": question_id
        })
      
    
    def get_unanswered_questions_number(not_covered_questions=False):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        filter = {
            "answer_text": ""
        }
        
        if not_covered_questions:
            filter["is_covered"] = False
        
        return len(list(collection.find(filter)))
    
        
        
class Question:
    def __init__(self, question_id: str, data=None) -> None:
        
        if not data:
            question_data = Question.__get_question_data(question_id)
        
            if not question_data:
                raise ValueError(f"No question with next question_id: {question_id}")
        
        else:
            question_data = data

        self.__question_id = question_data["question_id"]
        self.__user_id = question_data["user_id"]
        self.__question_text = question_data["question_text"]
        self.__author = question_data["author"]
        self.__answer_text = question_data["answer_text"]
        self.__answer_author = question_data["answer_author"]
        self.__is_covered = question_data["is_covered"]
    
    
#region properties
    @property
    def question_id(self):
        return self.__question_id
    
    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def question_text(self):
        return self.__question_text
    
    @property
    def author(self):
        return self.__author
    
    @property
    def answer_text(self):
        return self.__answer_text
    
    @answer_text.setter
    def answer_text(self, value):
        Question.__update_question_data(self.__question_id, {
            "answer_text": value
        })
        self.__answer_text = value
    
    
    
    @property
    def answer_author(self):
        return self.__answer_author
    
    @answer_author.setter
    def answer_author(self, value):
        Question.__update_question_data(self.__question_id, {
            "answer_author": value
        })
        self.__answer_author = value
    
    
    
    @property
    def is_covered(self):
        return self.__is_covered
    
    @is_covered.setter
    def is_covered(self, value):
        Question.__update_question_data(self.__question_id, {
            "is_covered": value
        })
        self.__is_covered = value
#endregion

    def answer_question(self, answer_text: str, answer_author: str):
        Question.__update_question_data(self.question_id, {
                    "answer_text": answer_text, 
                    "answer_author": answer_author                   
                })
        
        self.__answer_text = answer_text
        self.__answer_author = answer_author
        

        
    def __get_question_data(question_id: str):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        return collection.find_one({
            "question_id": question_id
        })
    
    
    
    def __update_question_data(question_id: str, data: dict):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_QUESTIONS_COLLECTION_NAME]
        
        collection.update_one({
            "question_id": question_id
        }, {
            "$set": data
        })    
    
    
    def from_data(data: dict):
        return Question(question_id="", data=data)
    
        
class User:
    def __init__(self, user_id) -> None:
        self.__manipulator = DBManipulator(MONGO_DB_URI_FOR_CLIENT, MONGO_DB_NAME, MONGO_DB_USERS_COLLECTION_NAME)
        
        self.__user_id = user_id
        
        data = self.__get_user_data(user_id)
        
        if not data:
            raise ValueError(f"No user with next user_id: {user_id}") 
        
        self.__username = data["username"]
        self.__total_asked = data["total_asked"]
        self.__total_answered = data["total_answered"]
        self.__current_chat_id = data["current_chat_id"]
        
        
        
    def __get_user_data(self, user_id: str):
        return self.__manipulator.get_data({"user_id": user_id})
        
        
        
class Admin:
    def __init__(self, user_id: int) -> None:
        self.__manipulator = DBManipulator(MONGO_DB_URI_FOR_CLIENT, MONGO_DB_NAME, MONGO_DB_ADMINS_COLLECTION_NAME)
        self.__user_id = user_id
        
        data = self.__get_admin_data(user_id)
        
        if not data:
            raise ValueError(f"No admin with next user_id: {user_id}")
        
        self.__username = data["username"]
        self.__current_question_id = data["current_question_id"]
        
        
        
        
    def __update_admin_data(self, user_id: str, data: dict) -> None:
        self.__manipulator.set_data({
            "user_id": user_id
        }, {
            "$set": data
        })
        
    
    def __get_admin_data(self, user_id: str):
        return self.__manipulator.get_data({
            "user_id": user_id
        })
    
    
    
    
    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value):
        raise ValueError("user_id property cannot be changed")
    
    
    
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, value):
        Admin.__update_admin_data(self.__user_id, {
            "username": value
        })
        self.__username = value
    
    
        
    @property
    def current_question_id(self):
        return self.__current_question_id
    
    @current_question_id.setter
    def current_question_id(self, value):
        Admin.__update_admin_data(self.__user_id, {
            "current_question_id": value
        })
        self.__current_question_id = value



    def skip_current_question(self):
        self.uncover_current_question()
        self.current_question_id = ""



    def add_admin(user_id: int, username: str):
        manipulator = DBManipulator(MONGO_DB_URI_FOR_CLIENT, MONGO_DB_NAME, MONGO_DB_ADMINS_COLLECTION_NAME)
        
        manipulator.insert_data({
            "user_id": user_id,
            "username": username,
            "current_qustion_id": ""
        })



    def check_if_admin(user_id: str):
        manipulator = DBManipulator(MONGO_DB_URI_FOR_CLIENT)
        
        return bool(manipulator.get_data({
            "user_id": user_id
        }))
        
        
        
    
    def cover_current_question(self):
        question = Question(self.__current_question_id)
        question.is_covered = True



    def uncover_current_question(self):
        question = Question(self.__current_question_id)
        question.is_covered = False
        
        
        
    def answer_current_question(self, text) -> Question:
        question = Question(self.__current_question_id)
        question.answer_question(text, self.__username)
        question.is_covered = False
        
        return question
    
    
    
    def require_random_question(self) -> Question:
        user_question = UserQuestions.get_random_unanswered_question()
        
        if user_question:
            self.current_question_id = user_question.question_id
            user_question.is_covered = True
        
        return user_question
    
    
    
    def __get_admin_data(user_id: int):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_ADMINS_COLLECTION_NAME]
        
        return collection.find_one({
            "user_id": user_id
        })
    
    
    
    def __update_admin_data(user_id: int, data: dict):
        client = pymongo.MongoClient(MONGO_DB_URI_FOR_CLIENT)

        db = client[MONGO_DB_NAME]

        collection = db[MONGO_DB_ADMINS_COLLECTION_NAME]
        
        collection.update_one({
            "user_id": user_id
        }, {
            "$set": data
        })
        
        
        


class DBManipulator:
    def __init__(self, uri_for_client: str, db_name: str, collection_name: str) -> None:
        self.__client = pymongo.MongoClient(uri_for_client)
        
        self.__db = self.__client[db_name]
         
        self.__collection = self.__db[collection_name]
         
    
    
    def get_data(self, filter: dict, search_many=False):
        if search_many:
            return self.__collection.find(filter)
        
        return self.__collection.find_one(filter)
    
    
    
    def update_data(self, filter: dict, data: dict, update_many=False) -> None:
        if update_many:
            self.__collection.update_many(filter, data)
            return
            
        self.__collection.update_one(filter, {
            "$set": data
        })
    
    
    
    def set_data(self, filter: dict, data: dict, update_many=False) -> None:
        if update_many:
            self.__collection.update_many(filter, {
                "$set": data
            })
            return
        
        self.__collection.update_one(filter, {
            "$set": data
        })
        
    
    
    def insert_data(self, data: dict) -> None:
        self.__collection.insert_one(data)