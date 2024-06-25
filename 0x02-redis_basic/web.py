#!/usr/bin/env python3
"""
Obtain HTML content and returns it
"""

import redis
import requests
from functools import wraps
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator to count url requests"""

    @wraps(method)
    def wrapper(url):
        """wrapper for the decorator"""
        redis_.incr("count:{}".format(url))
        cached = redis_.get("cached:{}".format(url))
        if cached:
            return cached.decode("utf-8")
        html = method(url)
        redis_.setex("cached:{}".format(url), 10, html)
        return html

    return wrapper


def get_page(url: str) -> str:
    """
    Get HTML content of a web page
    """
    req = requests.get(url)
    return req.text
