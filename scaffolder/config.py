from __future__ import annotations

import os
import sys
from contextlib import suppress
from dataclasses import dataclass
from functools import cached_property, partial
from pathlib import Path
from shutil import rmtree
from typing import Literal, List

from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment
from pydantic_core import to_jsonable_python

from scaffolder.extensions import YieldExtension

DEFAULT_TEMPLATES_SUFFIX = ".jinja"
DEFAULT_EXCLUDE: List[str] = [
    "~*",
    "*.py[co]",
    "__pycache__",
    ".git",
    ".DS_Store",
    ".svn",
]

@dataclass
class Config:
    def __init__(self, src_path='', dst_path=''):
        self.cwd_path = Path('.')
        self.template_path = Path(src_path)
        self.dst_path = Path(dst_path)
        self.ex_patterns = DEFAULT_EXCLUDE

    def append_exclude_pattern(self, pattern: str):
        self.ex_patterns.append(pattern)

    @cached_property
    def templates_suffix(self) -> str:
        return DEFAULT_TEMPLATES_SUFFIX

    @cached_property
    def exclude_patterns(self):
        return self.ex_patterns

    @cached_property
    def template_abspath(self) -> Path:
        result = self.template_path
        if not result.is_dir():
            raise ValueError("Local template must be a directory.")
        with suppress(OSError):
            result = result.resolve()
        return result

    @cached_property
    def temp_dst_abspath(self) -> Path:
        result = self.cwd_path / f"{self.dst_path}-temporary"
        if not result.is_dir():
            result.mkdir()
        with suppress(OSError):
            result = result.resolve()
        return result

    @cached_property
    def dst_abspath(self) -> Path:
        result = self.cwd_path / self.dst_path
        if not result.is_dir():
            result.mkdir()
        with suppress(OSError):
            result = result.resolve()
        return result

    @cached_property
    def jinja_env(self):
        paths = [str(self.template_abspath)]
        loader = FileSystemLoader(paths)
        extensions = []
        env = SandboxedEnvironment(
            loader=loader, extensions=extensions
        )
        # patch the `to_json` filter to support Pydantic dataclasses
        # env.filters["to_json"] = partial(
        #     env.filters["to_json"], default=to_jsonable_python
        # )

        # Add a global function to join filesystem paths.
        separators = {
            "posix": "/",
            "windows": "\\",
            "native": os.path.sep,
        }

        def _pathjoin(
                *path: str, mode: Literal["posix", "windows", "native"] = "posix"
        ) -> str:
            return separators[mode].join(path)

        env.globals["pathjoin"] = _pathjoin
        env.add_extension(YieldExtension)
        return env