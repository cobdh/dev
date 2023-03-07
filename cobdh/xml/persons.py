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
    # TODO: THERE MUST BE A BETTER WAY
    use_ns = 'xmlns:tei' in content
    use_ns |= 'xmlns="http://www.tei-c.org/ns/1.0"' in content
    _namespace, _author, _surname, _forename = (
        NS if use_ns else None,
        './/tei:author' if use_ns else './/author',
        'tei:surname' if use_ns else 'surname',
        'tei:forename' if use_ns else 'forename',
    )
    result = []
    try:
        parsed = cobdh.xml.parser.parse(content)
    except ValueError:
        return None
    for author in parsed.findall(_author, namespaces=_namespace):
        surname = tuple(item.text for item in author.findall(
            _surname,
            namespaces=_namespace,
        ))
        forenames = tuple(item.text for item in author.findall(
            _forename,
            namespaces=_namespace,
        ))
        line = (surname, forenames)
        result.append(line)
    return result


def xml(person: tuple) -> str:
    r"""\
    >>> xml(('Hovhanessian Vahan', (('Hovhanessian',), ('Vahan',)))).replace('  ', '')
    '<person xml:id="HovhanessianVahan">\n<persName>\n<surname>Hovhanessian</surname>\n...'
    """
    assert isinstance(person, tuple), f'invalid input: {person} {type(person)}'
    xmlid = person[0].replace(' ', '')
    root = ET.Element('person', attrib={'xml:id': xmlid})
    pers = ET.SubElement(root, 'persName')
    surnames = person[1][0]
    for name in surnames:
        ET.SubElement(pers, 'surname').text = name
    forenames = person[1][1]
    for forename in forenames:
        ET.SubElement(pers, 'forename').text = forename
    result = cobdh.xml.inter.to_str(root)
    return result
