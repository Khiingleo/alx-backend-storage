#!/usr/bin/env python3
""" defines a class Cache """
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps

TypeUnion = Union[None, int, float, bytes, str]


def count_calls(method: Callable) -> Callable:
    """
    decorator that counts the number of times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> TypeUnion:
        key = method.__qualname__

        count = self._redis.incr(key)

        result = method(self, *args, **kwargs)

        return result

    return wrapper


def call_history(method: Callable) -> Callable:
    """ decorator that stores the history of input and outputs
    for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> TypeUnion:
        inputs_key = "{}:inputs".format(method.__qualname__)
        outputs_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(inputs_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(outputs_key, result)

        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    display the history of calls of a particular function
    """
    name = method.__qualname__
    inputs_key = name + ":inputs"
    outputs_key = name + ":outputs"

    inputs = method.__self__._redis.lrange(inputs_key, 0, -1)
    outputs = method.__self__._redis.lrange(outputs_key, 0, -1)

    print("{} was called {} times:".format(name, len(inputs)))
    for inp, out in zip(inputs, outputs):
        i = inp.decode("utf-8")
        o = out.decode("utf-8")
        print("{}(*{}) -> {}".format(name, i, o))


class Cache:
    """
    Cache class
    """
    def __init__(self) -> None:
        """
        the init method of stores the instance of redis in
        _redis and flushes the instance using flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
