import argparse
import pathlib
import sys

import cobdh.utils
import cobdh.xml.inter


def main() -> int:
    path, exts = evalcli()
    items = files(path, exts=exts)
    print('detected:')
    for path in items:
        print(path)
    if not items:
        print('nothing todo')
        return cobdh.utils.FAILURE
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
    return cobdh.utils.SUCCESS


def files(path, exts: str = 'xml'):
    path = pathlib.Path(path)
    result = [path]
    if not path.is_file():
        result = []
        for ext in exts.split():
            result += list(path.glob(f'**/*.{ext}'))
    return result


def evalcli():
    parser = argparse.ArgumentParser(
        prog='cob_xml',
        description='Format xml files.',
    )
    parser.add_argument(
        'src',
        help='directory or a single file',
        default='.',
        nargs='?',
    )
    parser.add_argument(
        '--ext',
        help='select file ext',
        nargs='?',
        default='xml'.split(),
        action='append',
    )
    args = parser.parse_args()
    path = args.src
    exts = ' '.join(list(set(args.ext)))
    return path, exts
