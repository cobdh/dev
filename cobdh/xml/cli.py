import pathlib
import sys

import cobdh.utils
import cobdh.xml.inter

SUCCESS = 0
FAILURE = 1


def main() -> int:
    items = files()
    print('detected:')
    for path in items:
        print(path)
    if not items:
        print('nothing todo')
        return FAILURE
    for path in items:
        content = cobdh.utils.file_read(path)
        formatted = cobdh.xml.inter.xmlformat(content, header=True)
        if formatted == content:
            print(f'skip: {path}')
            continue
        print(f'format: {path}')
        cobdh.utils.file_replace(
            path,
            content=formatted,
        )
    return SUCCESS


def files():
    result = []
    path = sys.argv[-1] if len(sys.argv) > 1 else '.'
    path = pathlib.Path(path)
    result = [path]
    if not path.is_file():
        result = list(path.glob('**/*.xml'))
    return result
