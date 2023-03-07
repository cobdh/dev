import argparse
import os

import cobdh
import cobdh.xml.inter
import cobdh.xml.parser
import cobdh.xml.persons


def main():
    args = evalcli()
    dst = os.getcwd()
    src = args.src
    assert os.path.exists(src), src
    collection = list(cobdh.xml.persons.create(src).items())
    print(f'init persons: {len(collection)}')
    for index, value in enumerate(collection, start=1):
        outpath = os.path.join(dst, f'{index}.xml')
        print(f'{index}', end=' ')
        converted = cobdh.xml.persons.xml(value)
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
    parsed = cobdh.xml.parser.parse(content)
    result = []
    for item in parsed.findall(node):
        result.append(item)
    return result
