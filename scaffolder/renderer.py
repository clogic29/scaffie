import json
import shutil
from functools import cached_property
from pathlib import Path

from scaffolder.config import Config
from scaffolder.input import Input
from scaffolder.template import JinjaTemplate
from scaffolder.utils import scantree, match, is_yield, get_yield_key


class Renderer:
    def __init__(self, input: Input, config: Config):
        self.input = input
        self.config = config

    @cached_property
    def jinja_env(self):
        return self.config.jinja_env

    @cached_property
    def input_context(self):
        return self.input.data

    def run(self):
        self._prepare()
        # self._render()
        self._cleanup()

    def _prepare(self):
        context = self.input_context
        for src in scantree(str(self.config.template_abspath)):
            if match(self.config.exclude_patterns, src):
                continue

            src_abspath = Path(src.path)
            src_relpath = Path(src_abspath).relative_to(self.config.template_abspath)
            target_path = self.config.temp_dst_abspath / src_relpath
            if src.is_dir() and not target_path.exists():
                result = self._render_path(src.name, context=context)
                if not is_yield(self.jinja_env, src.name):
                    target_path.mkdir()
                    continue

                yield_key = get_yield_key(self.jinja_env, src.name)
                for key, value in result[yield_key].items():
                    yield_path = target_path.parent / key
                    shutil.copytree(src_abspath, yield_path)
                    local_context = yield_path / 'context.json'
                    local_context.touch()
                    local_context.write_text(json.dumps({yield_key: value}))
                self.config.append_exclude_pattern(f"*{src_relpath.name}*")

            if src.is_file() and not target_path.exists():
                target_path.touch()
                with open(src, 'r') as f:
                    target_path.write_text(f.read())

    def _render(self):
        context = self.input_context
        for src in scantree(str(self.config.temp_dst_abspath)):
            if match(self.config.exclude_patterns, src):
                continue



    def _cleanup(self):
        pass
        # shutil.rmtree(self.config.temp_dst_abspath)

    def _parse(self, relpath: Path):
        pass

    def _render_path(self, value: str, context: dict) -> str | dict:
        tpl = self.jinja_env.from_string(value)
        rendered = tpl.render(**context)
        try:
            return json.loads(rendered)
        except json.JSONDecodeError:
            return rendered

    def exclude_patterns(self):
        return self.config.exclude_patterns
