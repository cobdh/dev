import argparse

import cobdh
import cobdh.xml.enrich
import cobdh.xml.inter


def main() -> int:
    path = evalcli()
    items = cobdh.file_list(
        path,
        exts='xml',
    )
    print('detected:')
    for path in items:
        print(path)
    if not items:
        print('nothing todo')
        return cobdh.FAILURE
    for path in items:
        before = cobdh.file_read(path)
        content = cobdh.xml.enrich.enrich(before)
        if before != content:
            print(f'enrich: {path}')
        formatted = cobdh.xml.inter.xmlformat(
            content,
            header=True,
        )
        if formatted == before:
            print(f'skip: {path}')
            continue
        print(f'format: {path}')
        print()
        cobdh.file_replace(
            path,
            content=formatted,
        )
    return cobdh.SUCCESS


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
