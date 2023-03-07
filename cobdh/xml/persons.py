import collections
import xml.etree.ElementTree as ET

import cobdh
import cobdh.xml.inter
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


def xml(person: tuple) -> str:
    r"""\
    >>> xml(('Hovhanessian Vahan', (('Hovhanessian',), ('Vahan',)))).replace('  ', '')
    '<tei:person xml:id="HovhanessianVahan">\n<tei:persName>\n<tei:surname>Hovhanessian</tei:surname>\n...'
    """
    xmlid = person[0].replace(' ', '')
    root = ET.Element('tei:person', attrib={'xml:id': xmlid})
    pers = ET.SubElement(root, 'tei:persName')
    for name in person[1][0]:
        ET.SubElement(pers, 'tei:surname').text = name
    for forename in person[1][1]:
        ET.SubElement(pers, 'tei:forename').text = forename
    result = cobdh.xml.inter.to_str(root)
    return result
