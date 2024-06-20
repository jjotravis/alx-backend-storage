#!/usr/bin/env python3
"""
Return all students sorted by average score
The top must be ordered
average score returns with key = averageScore
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    Parameters:
    mongo_collection: MongoDB collection containing student data
    Returns:
    A cursor with all students sorted by average score in descending order
"""
    return mongo_collection.aggregate([
        {
            "$project":
            {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort":
            {
                "averageScore": -1
            }
        }
    ])
