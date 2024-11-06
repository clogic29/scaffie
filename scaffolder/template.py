from typing import Any

from jinja2 import Template


class JinjaTemplate(Template):
    def render_yield(self, *args: Any, **kwargs: Any) -> str:
        ctx = self.new_context(dict(*args, **kwargs))
        return self.root_render_func(ctx)