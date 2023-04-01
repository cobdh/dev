import argparse

import cobdh
import cobdh.xmlx.enrich
import cobdh.xmlx.inter


def main() -> int:
    path = evalcli()
    items = cobdh.file_list(
        path,
        exts='xml',
    )
    cobdh.scribe('detected:')
    for path in items:
        cobdh.scribe(path)
    if not items:
        cobdh.scribe('nothing todo')
        return cobdh.FAILURE
    for path in items:
        before = cobdh.file_read(path)
        content = cobdh.xmlx.enrich.enrich(before)
        if before != content:
            cobdh.scribe(f'enrich: {path}')
        formatted = cobdh.xmlx.inter.xmlformat(
            content,
            header=True,
        )
        if formatted == before:
            cobdh.scribe(f'skip: {path}')
            continue
        cobdh.scribe(f'format: {path}')
        cobdh.scribe()
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
