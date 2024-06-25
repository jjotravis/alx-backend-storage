#!/usr/bin/env python3
"""
Cache class
"""
import redis
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4


types = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator function to count the number of calls to a method.

    Parameters:
    - method (Callable): The method to be decorated.

    Returns:
    - Callable: wrapped method that increments a counter in Redis.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator function to keep track of the inputs and outputs of a method.

    Parameters:
    - method (Callable): The method to be decorated.

    Returns:
    - Callable: wrapped method that stores the inputs and outputs in Redis."""
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for call_history
        """
        self._redis.rpush(i, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(o, str(result))
        return result
    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Parameters:
    - method (Callable): The method to replay the history for.
    """
    self = method.__self__
    key = method.__qualname__
    inputs_key = "{}:inputs".format(key)
    outputs_key = "{}:outputs".format(key)

    call_count = self._redis.get(key)
    if call_count is None:
        call_count = 0
    else:
        call_count = int(call_count)

    print("{} was called {} times:".formats(key, call_count))

    inputs = self._redis.lrange(inputs_key, 0, -1)
    outputs = self._redis.lrange(outputs_key, 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key, input_data.decode('utf-8'),
                                     output_data.decode('utf-8')))


class Cache:
    """
    Class representing a cache system using Redis.

    Methods:
    - __init__: Initializes the Cache object
    - store: Stores the provided data in the cache with a unique key
    """

    def __init__(self):
        """
        Initializes the Cache object
        Connects to Redis server and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb

    @count_calls
    @call_history
    def store(self, data: types) -> str:
        """
        Stores the provided data in the cache with a unique key.

        Parameters:
        - data (Union[str, bytes, int, float]): data to be stored in cache.

        Returns:
        - str: The unique key under which the data is stored in the cache.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> types:
        """
        Retrieve data from the cache using the provided key.

        Parameters:
        - key (str): unique key under which the data is stored in the cache.
        - fn (Optional[Callable]): optional function to process retrieved data.

        Returns:
        - types: data stored in the cache corresponding to the provided key
        """
        if fn:
            return self._redis.get(key)
        data = self._redis.get(key)
        return data

    def det_int(self: bytes) -> int:
        """Get an integer"""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Get a string"""
        return self.decode("utf-8")
