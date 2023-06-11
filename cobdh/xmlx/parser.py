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


SIGNS = '|'.join(r'amp nbsp lt gt #\d{1,4} [a-z]{2,8}'.split())
PATTERN = re.compile('&(?!' + SIGNS + ';)')


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
    >>> fix_ampersand('<p>&gt;&gt; hello &#171;  &#037;</p>')
    '<p>&gt;&gt; hello &#171;  &#037;</p>'
    """
    text = PATTERN.sub('&amp;', text)
    return text
