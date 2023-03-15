import argparse
import os

import cobdh
import cobdh.xml.fix


def main():
    args = evalcli()
    src = args.src
    assert os.path.exists(src), src
    cobdh.xml.fix.xml_id(
        src=src,
        dst=src,
    )
    # format it
    cobdh.run('cob_xml --ext xml .')
    return cobdh.SUCCESS


def evalcli():
    parser = argparse.ArgumentParser(
        prog='cob_bibl',
        description='Fix xml ids',
    )
    parser.add_argument('src', help='Directory with bibliography data')
    args = parser.parse_args()
    return args
