#!/usr/bin/env python3
""" defines a class Cache """
import redis
import uuid
from typing import Union, Optional, Callable
TypeUnion = Union[None, int, float, bytes, str]


class Cache:
    """
    Cache class
    """
    def __init__(self) -> None:
        """cache class to interact with redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generates a random key and stores the input
        data in redis using the random key and returns the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> TypeUnion:
        """
        takes a string argument and an optional callable argument to
        convert the data back to the desired format
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        automatically parametrize Cache.get with the correct conversion
        (str)
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """
        automatically parametrize Cache.get with the correct conversion
        (int)
        """
        return self.get(key, int)
