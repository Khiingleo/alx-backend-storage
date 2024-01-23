#!/usr/bin/env python3
""" defines a function update_topics """
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a document based on the name

    Args:
        mongo_collection: a pymongo collection object
        name (string): name to update
        topics (list of strings): list of topics
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
