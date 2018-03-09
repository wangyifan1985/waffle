#!/usr/bin/env python
# coding: utf-8

import argparse
import copy
import sys
from . import __version__
from .util import to_dict, is_ipv4, is_ipv6, get_ip

__all__ = ['serve']


def _ensure_value(namespace, name, value):
    if getattr(namespace, name, None) is None:
        setattr(namespace, name, value)
    return getattr(namespace, name)


class _AppendListAction(argparse.Action):
    def __init__(self, item_separator=',', *args, **kwargs):
        self.item_sep = item_separator
        super(_AppendListAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        items = copy.copy(_ensure_value(namespace, self.dest, []))
        if self.item_sep in values:
            items.extend(values.split(self.item_sep))
        else:
            items.append(values)
        setattr(namespace, self.dest, items)


class _AppendDictAction(argparse.Action):
    def __init__(self, pair_separator=',', keyword_separator='=', *args, **kwargs):
        self.pair_sep, self.kw_sep = pair_separator, keyword_separator
        super(_AppendDictAction, self).__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        items = copy.copy(_ensure_value(namespace, self.dest, {}))
        if self.pair_sep in values:
            items.update(to_dict(values, self.pair_sep, self.kw_sep))
        else:
            items.setdefault(*(values.split(self.kw_sep, 1)))
        setattr(namespace, self.dest, items)


def _get_parser():
    _parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    _parser.add_argument('-v', '--version', action='store_true', help='Display version number.')
    _parser.add_argument('-b', '--bind', metavar='ADDRESS', default='0.0.0.0:8080', help='Bind socket to ADDRESS.')
    _parser.add_argument('-s', '--server', metavar='SERVER', default='default', help='Use SERVER as backend.')
    _parser.add_argument('-p', '--plugin', action=_AppendListAction, help='Install additional plugin.')
    _parser.add_argument('-c', '--conf', metavar='FILE', action=_AppendListAction, help='Load config values from FILE.')
    _parser.add_argument('-d', '--debug', action='store_true', help='Run server in debug mode.')
    _parser.add_argument('-a', '--args', metavar='NAME=VALUE', action=_AppendDictAction, help='Override config values.')

    return _parser


def serve():
    cmd_parser = _get_parser()
    cmd_args = cmd_parser.parse_args()

    if not cmd_args:
        cmd_parser.print_help()
        sys.exit(1)

    if cmd_args.version:
        print('Waffle web {}\nPython {}'.format(sys.version, __version__))
        sys.exit(0)

    if cmd_args.bind:
        if not is_ipv4(cmd_args.bind) or not is_ipv6(cmd_args.bind):
            print('Illegal bind address: {}\n'.format(cmd_args.bind))
            cmd_parser.print_help()
            sys.exit(1)
        _addr, _port = get_ip(cmd_args.bind)
        print('Waffle web bind: {}:{}'.format(_addr, _port))

    if cmd_args.server:
        print('Waffle web server: {}'.format(cmd_args.server))

    if cmd_args.plugin:
        print('Waffle web plugins: {}'.format(cmd_args.plugin))

    if cmd_args.conf:
        print('Waffle web conf: {}'.format(cmd_args.conf))

    if cmd_args.args:
        print('Waffle web extra args: {}'.format(cmd_args.args))

    if cmd_args.debug:
        print('Debug mode: {}'.format(cmd_args.debug))
