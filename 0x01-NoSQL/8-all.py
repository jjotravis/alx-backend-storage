#!/usr/bin/env python3
"""List all documents
"""


def list_all(mongo_collection):
    """
    list all documents in a collection
    """
    docs = mongo_collection.find()
    return docs
