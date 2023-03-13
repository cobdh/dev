import cobdh
import cobdh.xml.inter
import cobdh.xml.persons


def enrich(content: str) -> str:
    if require(content):
        content = inject_header(content)
    # do not expand tei: to full namespace
    cobdh.xml.inter.register_ns(content)
    content = inject_author_id(content)
    return content


def inject_header(content: str) -> str:
    # remove optional header of of content
    content = content.replace(
        cobdh.xml.inter.HEADER,
        '',
    )
    result = TEMPLATE % content
    return result


def inject_author_id(content: str) -> str:
    parsed = cobdh.xml_parse(content)
    namespaces = cobdh.xml.persons.NS
    for author in parsed.findall('.//tei:author', namespaces=namespaces):
        # TODO: THERE MUST BE A BETTER WAY
        if author.attrib.get('{http://www.w3.org/XML/1998/namespace}id', False):
            # xml:id already exists
            continue
        author_parsed = cobdh.xml.persons.parse_person(
            author,
            use_ns=True,
        )
        hashed = cobdh.xml.persons.person_hash(author_parsed)
        if not hashed:
            print(f'[ERROR]: could not hash: {author_parsed}')
            continue
        author.attrib['xml:id'] = hashed
    result = cobdh.xml_tostr(
        parsed,
        header=False,
    )
    return result


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
