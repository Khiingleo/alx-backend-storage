#!/usr/bin/env python3
""" defines a function top_students """
from pymongo import MongoClient


def top_students(mongo_collection):
    """
    returns all students sorted by average score
    """
    documents = list(mongo_collection.find())
    for doc in documents:
        total = 0
        for topic in doc["topics"]:
            total += topic["score"]
        average = total / len(doc["topics"])

        name = doc["name"]
        avg_ = {"averageScore": average}
        mongo_collection.update_many({"name": name}, {"$set": avg_})

    return mongo_collection.find().sort("averageScore", -1)
