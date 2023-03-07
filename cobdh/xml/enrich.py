import cobdh.xml.inter


def enrich(content: str) -> str:
    # remove optional header of of content
    content = content.replace(
        cobdh.xml.inter.HEADER,
        '',
    )
    result = TEMPLATE % content
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
