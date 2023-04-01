import cobdh
import cobdh.xmlx.inter
import cobdh.xmlx.persons
import cobdh.xmlx.persons.parser


def enrich(content: str) -> str:
    if require(content):
        content = inject_header(content)
    # do not expand tei: to full namespace
    cobdh.xmlx.inter.register_ns(content)
    content = inject_author_id(content)
    return content


def inject_header(content: str) -> str:
    # remove optional header of of content
    content = content.replace(
        cobdh.xmlx.inter.HEADER,
        '',
    )
    result = TEMPLATE % content
    return result


def inject_author_id(content: str) -> str:
    parsed = cobdh.xml_parse(content)
    namespaces = cobdh.xmlx.persons.NS
    # TODO: IMPROVE IF XPATH CAN HANDLE MULTIPLE ONE
    todos = (parsed.findall('.//tei:author', namespaces=namespaces) +
             parsed.findall('.//tei:editor', namespaces=namespaces))
    for author in todos:
        # TODO: THERE MUST BE A BETTER WAY
        if author.attrib.get('{http://www.w3.org/XML/1998/namespace}id', False):
            # xml:id already exists
            continue
        author_parsed = cobdh.xmlx.persons.parser.parse_person(
            author,
            use_ns=True,
        )
        hashed = author_parsed.xmlid
        if not hashed:
            cobdh.error(f'could not hash: {author_parsed}')
            continue
        author = author_add_id(
            author,
            hashed=hashed,
        )
    result = cobdh.xml_tostr(
        parsed,
        header=False,
    )
    result = cobdh.xml_format(
        result,
        header=False,
    )
    return result


def author_add_id(author, hashed: str):
    ref = f'https://cobdh.org/persons/{hashed}'
    author.attrib['xml:id'] = hashed
    author.attrib['ref'] = ref
    return author


TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<TEI
    xmlns="http://www.tei-c.org/ns/1.0"
    xml:lang="en"
>
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <editor
                    xml:id="schewe_helmut_konrad"
                    ref="https://cobdh.org/editors/schewe_helmut_konrad"
                    role="creator"
                />
            </titleStmt>
        </fileDesc>
    </teiHeader>
    <body>
    %s
    </body>
</TEI>
"""


def require(content: str) -> bool:
    """\
    >>> require(TEMPLATE)
    False
    """
    if '<teiHeader>' in content:
        return False
    return True
