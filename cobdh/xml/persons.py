import collections

import cobdh
import cobdh.xml.parser


def create(path: str) -> dict:
    result = collections.OrderedDict()
    sources = cobdh.file_list(path)
    for src in sources:
        content = cobdh.file_read(src)
        parsed = parse(content)
        if parsed is None:
            print(f'[ERROR]: could not parse: {src}')
            continue
        if not parsed:
            print(f'[ERROR]: could not find author: {src}')
            continue
        for person in parsed:
            hashed = ' '.join(person[0]) + ' '
            hashed += ' '.join(person[1])
            result[hashed] = person
    return result


NS = {
    'tei': 'http://www.tei-c.org/ns/1.0',
}


def parse(content: str) -> list:
    result = []
    try:
        parsed = cobdh.xml.parser.parse(content)
    except ValueError:
        return None
    for author in parsed.findall('.//tei:author', namespaces=NS):
        surname = tuple(item.text for item in author.findall(
            'tei:surname',
            namespaces=NS,
        ))
        forenames = tuple(item.text for item in author.findall(
            'tei:forename',
            namespaces=NS,
        ))
        line = (surname, forenames)
        result.append(line)
    return result
