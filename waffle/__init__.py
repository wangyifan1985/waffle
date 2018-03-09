#!/usr/bin/env python
# coding: utf-8


__author__ = ['Yifan Wang <yifan_wang@silanis.com>']
__copyright__ = "Copyright (C) 2017, The Waffle Authors"
__license__ = "MIT"
__version__ = '0.1.0'
__description__ = 'Python Web Toolkit'
__status__ = "Internal"


def check_environment():
    import platform
    if platform.python_version_tuple() < ('3', '6') or platform.python_implementation() != 'CPython':
        raise RuntimeError('Waffle requires CPython 3.6 or greater.')


check_environment()


# Constants ###################################################################
###############################################################################
ENCODING = 'utf-8'
BUFFER_SIZE = 8192
RFC_822_DATETIME = '%a, %d %b %Y %H:%M:%S GMT'

LF = '\n'
CRLF = '\r\n'
TAB = '\t'
SPACE = ' '
COLON = ':'
SEMICOLON = ';'
EMPTY = ''
SHARP = '#'
QUESTION = '?'
ASTERISK = '*'
SLASH = '/'
BACKSLASH = '\\'
UNDERSCORE = '_'
HYPHEN = '-'

ENC_LF = LF.encode(ENCODING)
ENC_CRLF = CRLF.encode(ENCODING)
ENC_TAB = TAB.encode(ENCODING)
ENC_SPACE = SPACE.encode(ENCODING)
ENC_COLON = COLON.encode(ENCODING)
ENC_SEMICOLON = SEMICOLON.encode(ENCODING)
ENC_EMPTY = EMPTY.encode(ENCODING)
ENC_SHARP = SHARP.encode(ENCODING)
ENC_QUESTION = QUESTION.encode(ENCODING)
ENC_ASTERISK = ASTERISK.encode(ENCODING)
ENC_SLASH = SLASH.encode(ENCODING)
ENC_BACKSLASH = BACKSLASH.encode(ENCODING)
ENC_UNDERSCORE = UNDERSCORE.encode(ENCODING)
ENC_HYPHEN = HYPHEN.encode(ENCODING)


HTTP_STATUS = {
    # 1xx Informational
    100: '100 Continue',
    101: '101 Switching Protocols',
    102: '102 Processing',

    # 2xx Success
    200: '200 OK',
    201: '201 Created',
    202: '202 Accepted',
    203: '203 Non-Authoritative Information',
    204: '204 No Content',
    205: '205 Reset Content',
    206: '206 Partial Content',
    207: '207 Multi-Status',
    208: '208 Already Reported',
    226: '226 IM Used',

    # 3xx Redirection
    300: '300 Multiple Choices',
    301: '301 Moved Permanently',
    302: '302 Found',
    303: '303 See Other',
    304: '304 Not Modified',
    305: '305 Use Proxy',
    307: '307 Temporary Redirect',
    308: '308 Permanent Redirect',

    # 4xx Client Error
    400: '400 Bad Request',
    401: '401 Unauthorized',
    402: '402 Payment Required',
    403: '403 Forbidden',
    404: '404 Not Found',
    405: '405 Method Not Allowed',
    406: '406 Not Acceptable',
    407: '407 Proxy Authentication Required',
    408: '408 Request Time-out',
    409: '409 Conflict',
    410: '410 Gone',
    411: '411 Length Required',
    412: '412 Precondition Failed',
    413: '413 Request Entity Too Large',
    414: '414 URI Too Long',
    415: '415 Unsupported Media Type',
    416: '416 Range Not Satisfiable',
    417: '417 Expectation Failed',
    418: "418 I'm a teapot",
    421: '421 Misdirected Request',
    422: '422 Unprocessable Entity',
    423: '423 Locked',
    424: '424 Failed Dependency',
    426: '426 Upgrade Required',
    428: '428 Precondition Required',
    429: '429 Too Many Requests',
    431: '431 Request Header Fields Too Large',
    451: '451 Unavailable For Legal Reasons',

    # 5xx Server Error
    500: '500 Internal Server Error',
    501: '501 Not Implemented',
    502: '502 Bad Gateway',
    503: '503 Service Unavailable',
    504: '504 Gateway Time-out',
    505: '505 HTTP Version not supported',
    506: '506 Variant Also Negotiates',
    507: '507 Insufficient Storage',
    508: '508 Loop Detected',
    510: '510 Not Extended',
    511: '511 Network Authentication Required'
}


# Errors ######################################################################
###############################################################################
class WaffleError(Exception):
    pass



