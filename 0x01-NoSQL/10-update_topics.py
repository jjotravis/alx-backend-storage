#!/usr/bin/env python3
"""
Changes all topics of a school document
"""


def update_topics(mongo_collection, name, topics):
    """
    Change all topics based on the name
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
