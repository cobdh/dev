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
    overwrite = args.force
    create_persons(
        dst,
        src,
        overwrite=overwrite,
    )
    cobdh.run('cob_enrich .')
    return cobdh.SUCCESS


def create_persons(dst, src, overwrite: bool = False):
    collection = list(cobdh.xmlx.persons.create(src).items())
    cobdh.scribe(f'init persons: {len(collection)}')
    for path in pathgenerator(collection, dst, overwrite):
        if not path:
            continue
        value, index, outpath = path
        cobdh.scribe(f'{index}', end=' ')
        converted = cobdh.xmlx.persons.xml(value)
        cobdh.file_replace(
            outpath,
            content=converted,
        )
    cobdh.scribe('done')


def pathgenerator(collection, dst, overwrite):
    if overwrite:
        for index, value in enumerate(collection, start=1):
            outpath = os.path.join(dst, f'{index}.xml')
            yield value, index, outpath
        return
    parsed = cobdh.xmlx.persons.persons_list(dst)
    done = {int(cobdh.file_name(value)) for value in parsed.values()}
    index = 1
    # TODO: REWRITE THIS CRAZY PEACE OF CODE
    for value in collection:
        xmlid = value[0].strip()
        if not xmlid:
            cobdh.scribe(f'[ERROR]: invalid xmlid: {value}\n')
            yield None
        if xmlid in parsed:
            # path already exists
            yield None
        while index in done:
            index += 1
        outpath = os.path.join(dst, f'{index}.xml')
        yield value, index, outpath
        index += 1


def evalcli():
    parser = argparse.ArgumentParser(
        prog='cob_persons',
        description='Generate person data based on bibliography',
    )
    parser.add_argument('src', help='Directory with bibliography data')
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing persons, if not extend persons database',
    )
    args = parser.parse_args()
    return args


def split(content: str, node: str) -> list:
    parsed = cobdh.xmlx.parser.parse(content)
    result = []
    for item in parsed.findall(node):
        result.append(item)
    return result
