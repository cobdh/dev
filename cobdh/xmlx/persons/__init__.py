import collections
import xml.etree.ElementTree as ET  # nosec

import cobdh
import cobdh.xmlx
import cobdh.xmlx.inter
import cobdh.xmlx.parser
import cobdh.xmlx.persons.magic


def create(path: str) -> dict:
    result = collections.OrderedDict()
    sources = cobdh.file_list(path)
    for src in sources:
        content = cobdh.file_read(src)
        parsed = parse(content)
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


def parse(content: str) -> list:
    todo = find_persons(content)
    if not todo:
        return todo
    use_ns = 'xmlns:tei' in content
    use_ns |= 'xmlns="http://www.tei-c.org/ns/1.0"' in content
    result = []
    for person in todo:
        line = parse_person(
            person,
            use_ns=use_ns,
        )
        if not line:
            raw = [item.text for item in person]
            cobdh.scribe(f'could not find names: {raw} {person.attrib}')
            continue
        result.append(line)
    return result


def find_persons(content: str) -> list:
    """Determine persons inside `author` tag. Expand multiple `persName`."""
    # TODO: THERE MUST BE A BETTER WAY
    use_ns = 'xmlns:tei' in content
    use_ns |= 'xmlns="http://www.tei-c.org/ns/1.0"' in content
    _namespace, _author, _editor = (
        NS if use_ns else None,
        './/tei:author' if use_ns else './/author',
        './/tei:monogr/tei:editor' if use_ns else './/monogr/editor',
    )
    try:
        parsed = cobdh.xmlx.parser.parse(content)
    except ValueError:
        return None
    todo = (parsed.findall(_author, namespaces=_namespace) +
            parsed.findall(_editor, namespaces=_namespace))
    result = []
    for item in todo:
        if 'persName' in str(list(item)):
            # <author ref="http://syriaca.org/person/372">
            # <persName xml:lang="en">
            #     <forename>Ignatius</forename>
            #     <forename>Afram</forename>
            #     <surname>Barsoum</surname>
            # </persName>
            #     <persName xml:lang="ar">
            #         <forename>اغناطيوس</forename>
            #         <forename>افرام</forename>
            #         <addName>الاول</addName>
            #         <surname>برصوم</surname>
            #     </persName>
            # </author>
            for person in item:
                result.append(person)
        else:
            result.append(item)
    return result


def parse_person(author, use_ns: bool = False) -> tuple:
    _namespace, _surname, _forename = (
        NS if use_ns else None,
        'tei:surname' if use_ns else 'surname',
        'tei:forename' if use_ns else 'forename',
    )
    surname = tuple(item.text for item in author.findall(
        _surname,
        namespaces=_namespace,
    ))
    forenames = tuple(item.text for item in author.findall(
        _forename,
        namespaces=_namespace,
    ))
    result = (surname, forenames)
    if not surname and not forenames:
        # TODO: HACKY
        if name := tuple(item.text for item in author):
            # <editor>
            #     <name>Idem</name>
            # </editor>
            result = (name, ())
            return result
        if not author.text or not author.text.strip():
            return None
        if simple := cobdh.xmlx.persons.magic.simple_name(author.text.strip()):
            # <author>\n    Blain, Virginia     \n</author>  # strip it
            # <author>Blain, Virginia</author>
            return simple
        result = ((author.text.strip()), ())
    return result


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
