import argparse

import cobdh
import cobdh.xmlx.validate.persons


def main() -> int:
    path = evalcli()
    cobdh.scribe('validate persons')
    cobdh.xmlx.validate.persons.validate(cobdh.join(path, 'persons'))
    return cobdh.SUCCESS


def evalcli():
    parser = argparse.ArgumentParser(prog='cob_validate')
    parser.add_argument(
        'src',
        help='directory',
        default='.',
    )
    args = parser.parse_args()
    path = args.src
    return path
