#!/usr/bin/env python3
""" defines the function schools_by_topic """
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """
    returns a list of schools having a specific topic
    """
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
