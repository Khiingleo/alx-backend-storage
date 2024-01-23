#!/usr/bin/env python3
""" defines a function insert_school """
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    inserts a new document into a MongoDB collection based on kwargs

    Args:
        mongo_collection: a pymongo collection object
        kwargs: keyword arguments representing the keys and values
                of the new document
    Returns:
        the new _id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
