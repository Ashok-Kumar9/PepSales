from pymongo import MongoClient
from bson import ObjectId
from app.config import Config

client = MongoClient(Config.MONGO_URI)
db = client.pepsales_db

class Question:
    def __init__(self, question, count=1, answer="", analysis="", rating=None):
        self.question = question
        self.count = count
        self.answer = answer
        self.analysis = analysis
        self.rating = rating

    def save(self):
        question_data = {
            "question": self.question,
            "count": self.count,
            "answer": self.answer,
            "analysis": self.analysis,
            "rating": self.rating
        }
        return db.questions.insert_one(question_data).inserted_id

    @staticmethod
    def get_top_questions(limit=5):
        questions = list(db.questions.find().sort("count", -1).limit(limit))
        return [Question.to_dict(q) for q in questions]

    @staticmethod
    def to_dict(question):
        return {
            "id": str(question["_id"]),
            "question": question["question"],
            "count": question["count"],
            "answer": question["answer"],
            "analysis": question["analysis"],
            "rating": question["rating"]
        }

    @staticmethod
    def get_by_id(question_id):
        question = db.questions.find_one({"_id": ObjectId(question_id)})
        return Question.to_dict(question) if question else None

    @staticmethod
    def update_rating(question_id, rating):
        db.questions.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": {"rating": rating}}
        )