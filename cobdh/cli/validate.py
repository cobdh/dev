import argparse

import cobdh
import cobdh.xmlx.validate.bibl
import cobdh.xmlx.validate.persons


def main() -> int:
    path, persons, bibl = evalcli()
    if persons:
        cobdh.scribe('validate persons')
        cobdh.xmlx.validate.persons.validate(cobdh.join(path, 'persons'))
    if bibl:
        cobdh.scribe('validate bibl')
        cobdh.xmlx.validate.bibl.validate(cobdh.join(path, 'bibl'))
    if not any((persons, bibl)):
        cobdh.error('nothing todo')
        return cobdh.FAILURE
    return cobdh.SUCCESS


def evalcli():
    parser = argparse.ArgumentParser(prog='cob_validate')
    parser.add_argument(
        'src',
        help='directory',
        default='.',
    )
    parser.add_argument('--persons', action='store_true')
    parser.add_argument('--bibl', action='store_true')
    args = parser.parse_args()
    path = args.src
    return path, args.persons, args.bibl
