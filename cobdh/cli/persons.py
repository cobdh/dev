import argparse
import os

import cobdh
import cobdh.xmlx.inter
import cobdh.xmlx.parser
import cobdh.xmlx.persons


def main():
    args = evalcli()
    dst = os.getcwd()
    src = args.src
    assert os.path.exists(src), src
    collection = list(cobdh.xmlx.persons.create(src).items())
    print(f'init persons: {len(collection)}')
    for index, value in enumerate(collection, start=1):
        outpath = os.path.join(dst, f'{index}.xml')
        print(f'{index}', end=' ')
        converted = cobdh.xmlx.persons.xml(value)
        cobdh.file_replace(
            outpath,
            content=converted,
        )
    cobdh.run('cob_enrich .')
    return cobdh.SUCCESS


def evalcli():
    parser = argparse.ArgumentParser(
        prog='cob_persons',
        description='Generate person data based on bibliography',
    )
    parser.add_argument('src', help='Directory with bibliography data')
    args = parser.parse_args()
    return args


def split(content: str, node: str) -> list:
    parsed = cobdh.xmlx.parser.parse(content)
    result = []
    for item in parsed.findall(node):
        result.append(item)
    return result
