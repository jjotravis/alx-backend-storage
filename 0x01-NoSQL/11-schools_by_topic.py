#!/usr/bin/env python3
"""
List of schools with specific topics
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns list of schools having specific topic
    """
    return mongo_collection.find({"topics": topic})
