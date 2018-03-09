#!/usr/bin/env python
# coding: utf-8

import os
import inspect
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler


__all__ = ['get_logger']


LOG_LEVEL = logging.INFO
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'Waffle.log')


class CustomFormatter(Formatter):
    LOG_FORMAT = '[%(asctime)s][%(levelname)s][%(name)s:%(lineno)d]: %(message)s'
    DATE_FORMAT = '%d/%m/%y %H:%M:%S'

    def __init__(self, fmt=LOG_FORMAT, datefmt=DATE_FORMAT):
        super(CustomFormatter, self).__init__(datefmt=datefmt)
        self._fmt = fmt
        self._normal = ''

    @staticmethod
    def _to_str(obj, enc='utf8'):
        if not isinstance(obj, bytes):
            if isinstance(obj, str):
                return obj
            raise TypeError
        return obj.decode(enc)

    def format(self, record):
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        formatted = self._fmt % record.__dict__
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            lines = [formatted.rstrip()]
            lines.extend(self._to_str(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted


class CustomFileHandler(RotatingFileHandler):
    MAX_BYTES = 1024*1024
    BACKUP_COUNT = 10
    ENCODING = 'utf8'

    def __init__(self, file_path, mode='a', max_bytes=MAX_BYTES, backup_count=BACKUP_COUNT, encoding=ENCODING, delay=0):
        _path = os.path.dirname(file_path)
        os.makedirs(_path, exist_ok=True)
        super(CustomFileHandler, self).__init__(file_path, mode, max_bytes, backup_count, encoding, delay)


def get_logger(name=None, level=LOG_LEVEL, log_file=LOG_FILE):
    _root = logging.getLogger()
    _root.setLevel(level)
    if not _root.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomFormatter())
        _root.addHandler(console_handler)
    if name:
        _custom = logging.getLogger(name)
    else:
        guess_module = inspect.getmodule(inspect.stack()[1][0])
        if guess_module.__name__ == '__main__':
            _name = os.path.splitext(os.path.basename(inspect.getfile(guess_module)))[0]
        else:
            _name = guess_module.__name__
        _custom = logging.getLogger(_name)
    if log_file:
        file_handler = CustomFileHandler(log_file)
        file_handler.setFormatter(CustomFormatter())
        _custom.addHandler(file_handler)
    return _custom
