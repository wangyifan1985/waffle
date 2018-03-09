#!/usr/bin/env python
# coding: utf-8

import re
import sys
import io
import json
import time
import datetime
from heapq import nlargest, nsmallest
from multiprocessing import pool, TimeoutError
from operator import itemgetter
from collections import abc
from itertools import repeat, chain, starmap
from functools import wraps
from threading import local
from . import RFC_822_DATETIME

__all__ = [
    'exec_in', 'to_str', 'to_bytes', 'to_dict', 'is_ipv4', 'is_ipv6', 'is_port', 'get_ip',
    'json_dumps', 'json_loads', 'get_file_size', 'squeeze'
]


# Functions ###################################################################
###############################################################################
def is_ipv4(address):
    _count = address.count(':')
    if _count == 0:
        patt = re.compile(
            r'^(?:(?:2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?)[.]){3}(?:2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?)$')
        if patt.match(address):
            return True
        return False
    if _count == 1:
        try:
            host, port = address.split(':', 1)
            return is_ipv4(host) and 0 <= int(port) <= 65535
        except ValueError:
            return False
    return False


def is_ipv6(address):
    _count = address.count(']:')
    if _count == 0:
        patt = re.compile(
            '^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)(?:%25(?:[A-Za-z0-9\\-._~]|%[0-9A-Fa-f]{2})+)?$')
        if patt.match(address):
            return True
        return False
    if _count == 1 and address.startswith('['):
        try:
            host, port = address.split(']:', 1)
            return is_ipv6(host[1:]) and 0 <= int(port) <= 65535
        except ValueError:
            return False
    return False


def get_ip(address, default='0.0.0.0:8080'):
    if is_ipv4(address):
        host, port = address.split(':', 1)
        return host, int(port)
    elif is_ipv6(address):
        host, port = address.split(']:', 1)
        return host[1:], int(port)
    return tuple(default.split(':', 1))


def to_bytes(_str, encoding='utf8'):
    if not isinstance(_str, str):
        if isinstance(_str, bytes):
            return _str
        raise TypeError
    return _str.encode(encoding)


def to_str(_bytes, encoding='utf8'):
    if not isinstance(_bytes, bytes):
        if isinstance(_bytes, str):
            return _bytes
        raise TypeError
    return _bytes.decode(encoding)


def to_dict(_str, pair_sep=',', kv_sep='='):
    """
    Convert string to dict
    :param _str: str
        Example:
            a=5,b=6,c=abc
    :param pair_sep: separator for each pair
    :param kv_sep: separator for key and value
    :return: dict
    """
    if not isinstance(_str, str):
        raise TypeError
    return {item[0].strip(): item[1].strip() for item in
            [_item.strip().split(kv_sep, 1) for _item in _str.split(pair_sep) if kv_sep in _item]}


def json_loads(js):
    if not isinstance(js, bytes):
        if isinstance(js, str):
            return json.loads(js)
        raise TypeError
    return json.loads(to_str(js))


def json_dumps(obj):
    return json.dumps(obj)


def datetime_to_str(dt=None):
    if isinstance(dt, datetime.datetime):
        return dt.strftime(RFC_822_DATETIME)
    elif isinstance(dt, int):
        return time.strftime(RFC_822_DATETIME, time.gmtime(dt))
    else:
        return time.strftime(RFC_822_DATETIME, time.gmtime())


def str_to_datetime(dt):
    return time.strptime(dt, RFC_822_DATETIME)


def timeout(max_timeout):
    """
    Timeout decorator, parameter in seconds.
    :param max_timeout: seconds to wait
    :return: wrapped function result
    """

    def timeout_decorator(func):
        """Wrap the original function."""

        @wraps(func)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            _pool = pool.ThreadPool(processes=1)
            async_result = _pool.apply_async(func, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            try:
                return async_result.get(max_timeout)
            except TimeoutError:
                return None

        return func_wrapper

    return timeout_decorator



def find_dict_key(obj, val):
    """
    Find all key for given value
    :param obj: dict
    :param val: value
    :return: list
    """
    result = []
    for k, v in obj.items():
        if v == val:
            result.append(k)
    return result


def increase_dict_val(obj, key):
    """
    Increase value by given key
    :param obj: dict
    :param key: key
    :return: value
    """
    obj.setdefault(key, 0)
    obj[key] += 1
    return obj[key]


def add_dict(*dicts):
    """
    Add dict
    :param dicts: dict
    :return: dict
    """
    result = {}
    for _dict in dicts:
        result.update(_dict)
    return result


def unique_list(obj, key=None):
    """
    Remove same element from list
    :param obj: list
    :param key: key function
    :return: list
    """
    checked = []
    seen = set()
    for e in obj:
        _e = key(e) if key else e
        if _e not in seen:
            checked.append(e)
            seen.add(_e)
    return checked


def requeue_list(obj, idx):
    """
    Returns the element at index after moving it to the beginning of the queue.
    :param obj: list
    :param idx: index
    :return: list
    """
    obj.insert(0, obj.pop(idx))
    return obj


def restack_list(obj, idx):
    """
    Returns the element at index after moving it to the top of stack.
    :param obj: list
    :param idx: index
    :return: list
    """
    obj.append(obj.pop(idx))
    return obj


def get_list_elem(obj, idx, dft):
    """
    Returns element at index or default
    :param obj: list
    :param idx: index
    :param dft: default value
    :return: element
    """
    if len(obj) - 1 < idx:
        return dft
    return obj[idx]


def get_int(obj, dft):
    """
    Returns int
    :param obj: str
    :param dft: default value
    :return: int
    """
    try:
        return int(obj)
    except (TypeError, ValueError):
        return dft


def format_digit(obj, key=None):
    """
    Format int base on key function
    :param obj: int
    :param key: function to be applied
    :return: formatted sting
    """
    return key(obj)


def ordinal_digit(obj):
    """
    Convert int to ordinal str
    :param obj: int
    :return: str
    """
    if not isinstance(obj, int):
        raise TypeError

    def ordinal(n): return '%d%s' % (n, 'tsnrhtdd'[(n / 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

    return format_digit(obj, ordinal)


def comma_digit(obj):
    """
    Add comma to digit dependent on digit places
    :param obj: int
    :return: digit string with comma
    """
    if not isinstance(obj, (int, float)):
        raise TypeError
    if isinstance(obj, int):
        return format_digit(obj, lambda n: '{:,}'.format(n))
    return format_digit(obj, lambda n: '{:,.2f}'.format(n))


def date_digit(obj):
    """
    Convert digit to datetime string
    :param obj: int
    :return: datetime string
    """
    if not isinstance(obj, (int, str)):
        raise TypeError
    _obj = str(obj)
    if len(_obj) != 14:
        raise ValueError

    def key_func(n):
        patt = 'XXXX-XX-XX XX:XX:XX'
        result = []
        item = list(n)
        for c in patt:
            if c == 'X':
                result.append(item.pop(0))
            else:
                result.append(c)
        return ''.join(result)

    return format_digit(str(obj), key_func)


def to_base36(obj):
    """
    Converts an integer to base 36 (a useful scheme for human-sayable IDs).
    :param obj: int
    :return: str
    """
    if obj < 0:
        raise ValueError('must supply a positive integer')
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    converted = []
    while obj != 0:
        obj, r = divmod(obj, 36)
        converted.insert(0, alphabet[r])
    return ''.join(converted) or '0'


def capture_output(func):
    def func_wrapper(*args, **kwargs):
        backup = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
            func(*args, **kwargs)
            out = sys.stdout.getvalue(), sys.stderr.getvalue()
        finally:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout, sys.stderr = backup

        return out

    return func_wrapper


def squeeze(s):
    """Replace all sequences of whitespace chars with a single space."""
    return re.sub(r"[\x00-\x20]+", " ", s).strip()


###############################################################################
# classes
###############################################################################
class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
        """

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        self[k] = v


class Counter(dict):
    """
    Counter class implemented by dict.
    """

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError('Expected at most 1 arguments, got {}.'.format(len(args)))
        super(Counter, self).__init__()
        self.update(*args, **kwargs)

    def __missing__(self, key):
        return 0

    @classmethod
    def fromkeys(cls, *args, **kwargs):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got {}'.format(len(args)))
        iterable = args[0] if args else None
        if iterable is not None:
            if isinstance(iterable, abc.Mapping):
                if self:
                    for elem, cnt in iterable.items():
                        self[elem] += cnt
                else:
                    super(Counter, self).update(iterable)
            else:
                for elem in str(iterable):
                    self[elem] += 1
        if kwargs:
            self.update(kwargs)

    def subtract(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got {}'.format(len(args)))
        iterable = args[0] if args else None
        if iterable is not None:
            if isinstance(iterable, abc.Mapping):
                if self:
                    for elem, cnt in iterable.items():
                        self[elem] -= cnt
            else:
                for elem in str(iterable):
                    self[elem] -= 1
        if kwargs:
            self.subtract(kwargs)

    def most_common(self, n=None):
        if n is None:
            return sorted(self.items(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.items(), key=itemgetter(1))

    def most(self):
        _, max_val = self.most_common(1)[0]
        return [(k, v) for k, v in self.items() if v == max_val]

    def least_common(self, n=None):
        if n is None:
            return sorted(self.items(), key=itemgetter(1))
        return nsmallest(n, self.items(), key=itemgetter(1))

    def least(self):
        _, min_val = self.least_common(1)[0]
        return [(k, v) for k, v in self.items() if v == min_val]

    def parent(self, key):
        return float(self[key]) / sum(self.values())

    def elements(self):
        return chain.from_iterable(starmap(repeat, self.items()))

    def copy(self):
        return self.__class__(self)

    def __reduce__(self):
        return self.__class__, (dict(self),)

    def __delitem__(self, key):
        if key in self:
            super(Counter, self).__delitem__(key)

    def __repr__(self):
        if not self:
            return '{}()'.format(self.__class__.__name__)
        return '{}({})'.format(self.__class__.__name__, dict.__repr__(self))

    def __add__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, cnt in self.items():
            newcnt = cnt + other[elem]
            if newcnt > 0:
                result[elem] = newcnt
        for elem, cnt in other.items():
            if elem not in self and cnt > 0:
                result[elem] = cnt
        return result

    def __sub__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, cnt in self.items():
            newcnt = cnt - other[elem]
            if newcnt > 0:
                result[elem] = newcnt
        for elem, cnt in other.items():
            if elem not in self and cnt < 0:
                result[elem] = 0 - cnt
        return result

    def __or__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, cnt in self.items():
            other_cnt = other[elem]
            newcnt = other_cnt if cnt < other_cnt else cnt
            if newcnt > 0:
                result[elem] = newcnt
        for elem, cnt in other.items():
            if elem not in self and cnt > 0:
                result[elem] = cnt
        return result

    def __and__(self, other):
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, cnt in self.items():
            other_cnt = other[elem]
            newcnt = cnt if cnt < other_cnt else other_cnt
            if newcnt > 0:
                result[elem] = newcnt
        return result


class ThreadedDict(local):
    _instances = set()

    def __init__(self):
        ThreadedDict._instances.add(self)

    def __del__(self):
        ThreadedDict._instances.remove(self)

    def __hash__(self):
        return id(self)

    @staticmethod
    def clear_all():
        """
            Clears all ThreadedDict instances.
        """
        for t in list(ThreadedDict._instances):
            t.clear()

    # Define all these methods to more or less fully emulate dict -- attribute access
    # is built into threading.local.

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    has_key = __contains__

    def clear(self):
        self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values

    def pop(self, key, *args):
        return self.__dict__.pop(key, *args)

    def popitem(self):
        return self.__dict__.popitem()

    def setdefault(self, key, default=None):
        return self.__dict__.setdefault(key, default)

    def update(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)

    def __repr__(self):
        return 'ThreadedDict {}'.format(local.__repr__(self))

    __str__ = __repr__
