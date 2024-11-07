import fnmatch
import os
from typing import Iterator, List, Set

from jinja2 import Environment


def scantree(path: str, follow_symlinks: bool = False) -> Iterator[os.DirEntry[str]]:
    """A recursive extension of `os.scandir`."""
    for entry in os.scandir(path):
        yield entry
        if entry.is_dir(follow_symlinks=follow_symlinks):
            yield from scantree(entry.path, follow_symlinks)


def match(patterns: Set[str], path: str) -> bool:
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


def get_file_paths_upwards(current_path: str, limit_path: str, filename: str) -> List[str]:
    files = []
    while current_path != limit_path:
        potential_file_path = os.path.join(current_path, filename)
        if os.path.isfile(potential_file_path):
            files.append(potential_file_path)
        current_path = os.path.dirname(current_path)
    return files
