"""\
This cli automates splitting of huge xml-files by a node-name, and write
them separate ascending xml-files.

cob_split -h
usage: cob_split [-h] [--src SRC] [--node NODE] [--index INDEX]

options:
  -h, --help     show this help message and exit
  --src SRC             data.xml
  --node NODE           .//biblStruct
  --index INDEX         12
"""
import argparse
import os

import cobdh.utils
import cobdh.xml.inter
import cobdh.xml.parser


def main():
    args = evalcli()
    root = os.getcwd()
    content = cobdh.utils.file_read(args.src)
    splitted = split(content, node=args.node)
    for index, value in enumerate(splitted, start=args.index):
        value = cobdh.xml.inter.to_str(value)
        formatted = cobdh.xml.inter.xmlformat(value)
        path = os.path.join(root, f'{index}.xml')
        print(f'{index}: {path}')
        cobdh.utils.file_create(
            path,
            content=formatted,
        )
    return cobdh.utils.SUCCESS


def evalcli():
    parser = argparse.ArgumentParser(
        prog='cob_split',
        description='Split xml-file into separate xml-files by node-name.',
    )
    parser.add_argument('--src', help='data.xml')
    parser.add_argument('--node', help='.//biblStruct')
    parser.add_argument('--index', type=int, default=1, help='12')
    args = parser.parse_args()
    return args


def split(content: str, node: str) -> list:
    parsed = cobdh.xml.parser.parse(content)
    result = []
    for item in parsed.findall(node):
        result.append(item)
    return result
