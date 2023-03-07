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

import cobdh
import cobdh.xml.inter
import cobdh.xml.parser


def main():
    args = evalcli()
    root = os.getcwd()
    content = cobdh.file_read(args.src)
    splitted = split(content, node=args.node)
    failure = cobdh.SUCCESS
    for index, value in enumerate(splitted, start=args.index):
        value = cobdh.xml.inter.to_str(value)
        try:
            formatted = cobdh.xml.inter.xmlformat(value)
        except ValueError:
            print(f'[ERROR]: could not create: {index}')
            failure += 1
            continue
        path = os.path.join(root, f'{index}.xml')
        print(f'{index}: {path}')
        cobdh.file_create(
            path,
            content=formatted,
        )
    return failure


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
