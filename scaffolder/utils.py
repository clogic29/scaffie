import fnmatch
import os
import typing
from typing import Iterator
from unicodedata import normalize

from jinja2 import Template, Environment


def scantree(path: str, follow_symlinks: bool = False) -> Iterator[os.DirEntry[str]]:
    """A recursive extension of `os.scandir`."""
    for entry in os.scandir(path):
        yield entry
        if entry.is_dir(follow_symlinks=follow_symlinks):
            yield from scantree(entry.path, follow_symlinks)


def match(patterns: typing.Set[str], path: str) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def is_yield(env: Environment, jinja_syntax: str):
    parsed = env.parse(jinja_syntax)
    try:
        return parsed.body[0].call.node.name == '_yield'
    except (IndexError, AttributeError):
        return False


def get_yield_key(env: Environment, jinja_syntax: str) -> str:
    parsed = env.parse(jinja_syntax)
    return parsed.body[0].call.args[0].value
