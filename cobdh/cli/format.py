import argparse

import cobdh
import cobdh.xml.inter


def main() -> int:
    path, exts = evalcli()
    items = cobdh.file_list(
        path,
        exts=exts,
    )
    print('detected:')
    for path in items:
        print(path)
    if not items:
        print('nothing todo')
        return cobdh.FAILURE
    for path in items:
        content = cobdh.file_read(path)
        formatted = cobdh.xml.inter.xmlformat(
            content,
            header=True,
        )
        if formatted == content:
            print(f'skip: {path}')
            continue
        print(f'format: {path}')
        cobdh.file_replace(
            path,
            content=formatted,
        )
    return cobdh.SUCCESS


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
