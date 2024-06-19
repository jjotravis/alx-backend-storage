#!/usr/bin/env python3
"""
Inserts a new Document
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert new document in a collection based on kwargs
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
