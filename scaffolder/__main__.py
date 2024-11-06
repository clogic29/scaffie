from scaffolder.config import Config
from scaffolder.input import Input
from scaffolder.renderer import Renderer

test_value = {
    'app': {"models": [
        {
            "name": "QWER",
            "fields": [
            ]
        },
        {
            "name": "PINK",
            "fields": [
            ]
        }
    ]
    }
}

src_path = 'tests/demo_yield_from'
dst_path = 'test1234'


if __name__ == '__main__':
    renderer = Renderer(Input(test_value), Config(src_path, dst_path))
    renderer.run()