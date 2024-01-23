#!/usr/bin/env python3
""" defines a function list_all """


def list_all(mongo_collection):
    """
    lists all documents in a pymongo collection object
    Returns:
        a list of all document in the collection
        an empty list if no document in the collection
    """
    documents = list(mongo_collection.find())
    if len(documents) == 0:
        return []
    return documents
