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
            result[person.xmlid] = person
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


def xml(person: 'cobdh.Person') -> str:
    r"""\
    >>> import cobdh;xml(cobdh.Person(names=(cobdh.Name(surname=('Hovhanessian',), forename=('Vahan',), lang='ar'),))).replace('  ', '')
    '<person xml:id="HovhanessianVahan">\n<persName xml:lang="ar">\n<surname>Hovhanessian</surname>\n...'
    """
    assert isinstance(person, cobdh.Person), f'invalid input: {person} {type(person)}'  # yapf:disable
    person = cobdh.xmlx.persons.magic.improve_name(person)
    xmlid = person.xmlid
    root = ET.Element('person', attrib={'xml:id': xmlid})
    for name in person.names:
        pers = ET.SubElement(root, 'persName')
        if name.lang != 'en':
            # non default lang
            pers.attrib['xml:lang'] = name.lang
        surnames = name.surname
        for surename in surnames:
            if surename.lower() in 'van der von zu':
                ET.SubElement(pers, 'nameLink').text = surename
            else:
                ET.SubElement(pers, 'surname').text = surename
        forenames = name.forename
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
    person = parsed.find('.//tei:person', namespaces=cobdh.xmlx.NS)
    if not person:
        cobdh.error(f'could not find tei:person {path}')
        return None
    xmlid = person.attrib.get(
        cobdh.xmlx.XML_ID,
        False,
    )
    if not xmlid:
        cobdh.error(f'could not find @xml:id {path}')
        return None
    return xmlid
