import cobdh
import cobdh.xmlx.persons.magic

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
