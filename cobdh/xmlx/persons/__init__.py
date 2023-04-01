import collections
import xml.etree.ElementTree as ET  # nosec

import cobdh
import cobdh.xmlx
import cobdh.xmlx.inter
import cobdh.xmlx.parser
import cobdh.xmlx.persons.magic
import cobdh.xmlx.persons.parser


def create(path: str) -> dict:
    result = collections.OrderedDict()
    sources = cobdh.file_list(path)
    for src in sources:
        content = cobdh.file_read(src)
        parsed = cobdh.xmlx.persons.parser.parse(content)
        if parsed is None:
            cobdh.error(f'could not parse: {src}')
            continue
        if not parsed:
            cobdh.error(f'could not find author: {src}')
            continue
        for person in parsed:
            hashed = person_hash(person)
            result[hashed] = person
    return result


def person_hash(person):
    """\
    >>> person_hash((('Hovhanessian',), ('Vahan A. B.', )))
    'HovhanessianVahanAB'
    """
    hashed = ' '.join(person[0]) + ' '
    hashed += ' '.join(person[1])
    hashed: str = cobdh.xmlx.clean_id(hashed)
    return hashed


NS = {
    'tei': 'http://www.tei-c.org/ns/1.0',
}


def xml(person: tuple) -> str:
    r"""\
    >>> xml(('Hovhanessian Vahan', (('Hovhanessian',), ('Vahan',)))).replace('  ', '')
    '<person xml:id="HovhanessianVahan">\n<persName>\n<surname>Hovhanessian</surname>\n...'
    """
    assert isinstance(person, tuple), f'invalid input: {person} {type(person)}'
    person = cobdh.xmlx.persons.magic.improve_name(person)
    xmlid = cobdh.xmlx.clean_id(person[0])
    root = ET.Element('person', attrib={'xml:id': xmlid})
    pers = ET.SubElement(root, 'persName')
    surnames = person[1][0]
    for name in surnames:
        if name.lower() in 'van der von zu':
            ET.SubElement(pers, 'nameLink').text = name
        else:
            ET.SubElement(pers, 'surname').text = name
    forenames = person[1][1]
    for forename in forenames:
        ET.SubElement(pers, 'forename').text = forename
    result = cobdh.xmlx.inter.to_str(root)
    return result


def persons_list(src: str) -> dict:
    result = {}
    for path in cobdh.file_list(src):
        content = cobdh.file_read(path)
        xmlid = parse_xmlid(content, path)
        if not xmlid:
            continue
        result[xmlid] = path
    return result


def parse_xmlid(content: str, path: str = None):
    # TODO: I DO NOT LIKE THIS
    parsed = cobdh.xml_parse(content)
    person = parsed.find('.//tei:person', namespaces=NS)
    if not person:
        cobdh.error(f'could not find tei:person {path}')
        return None
    xmlid = person.attrib.get(
        '{http://www.w3.org/XML/1998/namespace}id',
        False,
    )
    if not xmlid:
        cobdh.error(f'could not find @xml:id {path}')
        return None
    return xmlid
