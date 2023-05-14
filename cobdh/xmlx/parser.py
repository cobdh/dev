import re

from cobdh.xmlx.formatter import ET


def parse(raw: str):
    raw = fix_ampersand(raw)
    parsed = ET.fromstring(
        raw + '\n',
        parser_create(),
    )
    return parsed


def parser_create():
    parser = ET.XMLParser(target=ET.TreeBuilder(
        insert_comments=True,
        insert_pis=True,
    ))
    return parser


def fix_ampersand(text: str) -> str:
    """\
    >>> fix_ampersand('<title level="j">Scripta & e-Scripta</title>')
    '<title level="j">Scripta &amp; e-Scripta</title>'
    >>> fix_ampersand('&amp;')
    '&amp;'
    >>> fix_ampersand('&amp;&&&')
    '&amp;&amp;&amp;&amp;'
    >>> fix_ampersand('&&amp;')
    '&amp;&amp;'
    """
    # TODO: DO NOT COPY INSIDE <>
    text = re.sub('&(?!amp;)', '&amp;', text)
    return text
