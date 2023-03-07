import argparse
import pathlib

import cobdh.utils
import cobdh.xml.enrich
import cobdh.xml.inter


def main() -> int:
    path = evalcli()
    items = files(path)
    print('detected:')
    for path in items:
        print(path)
    if not items:
        print('nothing todo')
        return cobdh.utils.FAILURE
    for path in items:
        content = cobdh.utils.file_read(path)
        if cobdh.xml.enrich.require(content):
            print(f'enrich: {path}')
            content = cobdh.xml.enrich.enrich(content)
        formatted = cobdh.xml.inter.xmlformat(
            content,
            header=True,
        )
        if formatted == content:
            print(f'skip: {path}')
            continue
        print(f'format: {path}')
        print()
        cobdh.utils.file_replace(
            path,
            content=formatted,
        )
    return cobdh.utils.SUCCESS


def files(path):
    path = pathlib.Path(path)
    result = [path]
    if not path.is_file():
        result = list(path.glob(f'**/*.xml'))
    return result


def evalcli():
    parser = argparse.ArgumentParser(
        prog='cob_enrich',
        description='Inject TEI-header',
    )
    parser.add_argument(
        'src',
        help='directory or a single file',
        default='.',
        nargs='?',
    )
    args = parser.parse_args()
    path = args.src
    return path
