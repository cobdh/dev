import argparse

import cobdh
import cobdh.xmlx.inter


def main() -> int:
    path, exts = evalcli()
    items = cobdh.file_list(
        path,
        exts=exts,
    )
    cobdh.scribe('detected:')
    for path in items:
        cobdh.scribe(path)
    if not items:
        cobdh.scribe('nothing todo')
        return cobdh.FAILURE
    for path in items:
        content = cobdh.file_read(path)
        formatted = cobdh.xmlx.inter.xmlformat(
            content,
            header=True,
        )
        if formatted == content:
            cobdh.scribe(f'skip: {path}')
            continue
        cobdh.scribe(f'format: {path}')
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
