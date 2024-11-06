import json
import typing as t

from jinja2 import nodes
from jinja2.ext import Extension


class YieldExtension(Extension):
    tags = {'yield'}

    def parse(self, parser: "Parser") -> t.Union[nodes.Node, t.List[nodes.Node]]:
        lineno = next(parser.stream).lineno
        yield_value = parser.parse_assign_target()
        stream = parser.stream.expect('name:from')
        from_value = parser.parse_expression()
        body = parser.parse_statements(['name:endyield'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_yield', [nodes.Const(yield_value.name), from_value, nodes.Const(body[0].nodes[0].attr)]),
            [],
            [],
            body
        ).set_lineno(lineno)

    def _yield(self, yield_value, from_value, name, caller) -> str:
        result = {yield_value: {}}
        for item in from_value:
            result[yield_value][item[name]] = item
        return json.dumps(result)
