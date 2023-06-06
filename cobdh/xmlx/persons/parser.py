import cobdh
import cobdh.xmlx
import cobdh.xmlx.persons.magic


def parse(content: str) -> list:
    todo = find_persons(content)
    if not todo:
        return todo
    use_ns = 'xmlns:tei' in content
    use_ns |= 'xmlns="http://www.tei-c.org/ns/1.0"' in content
    result = []
    for person in todo:
        if isinstance(person, list):
            # multiple names
            line = [parse_person(item, use_ns=use_ns).names for item in person]
            # TODO: MAKE PARSER MORE ROBUST
            line = [item[0] for item in line if item]
            if line:
                line = cobdh.Person(names=line)
        else:
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
        cobdh.xmlx.NS if use_ns else None,
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
            result.append(list(item))
        else:
            result.append(item)
    return result


def parse_person(author, use_ns: bool = False) -> 'cobdh.Person':
    _namespace, _surname, _forename = (
        cobdh.xmlx.NS if use_ns else None,
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
    lang = parse_lang(author)
    person = cobdh.Person()
    if not surname and not forenames:
        # TODO: HACKY
        if name := tuple(item.text for item in author):
            # <editor>
            #     <name>Idem</name>
            # </editor>
            person.names.append(cobdh.Name(surname=name, lang=lang))
            return person
        if not author.text or not author.text.strip():
            return None
        if simple := cobdh.xmlx.persons.magic.simple_name(author.text.strip()):
            # <author>\n    Blain, Virginia     \n</author>  # strip it
            # <author>Blain, Virginia</author>
            person.names.append(
                cobdh.Name(
                    surname=simple[0],
                    forename=simple[1],
                    lang=lang,
                ))
            return person
        person.names.append(cobdh.Name(surname=[author.text.strip()]))
    person.names.append(
        cobdh.Name(
            surname=surname,
            forename=forenames,
            lang=lang,
        ))
    return person


def parse_lang(author) -> str:
    lang = author.attrib.get(
        cobdh.xmlx.XML_LANG,
        False,
    )
    if lang:
        return lang
    # default lang
    return 'en'
