import re

import cobdh.xml.parser
from cobdh.xml.formatter import ET

HEADER = '<?xml version="1.0" encoding="utf-8"?>'


def xmlformat(source: str, header: bool = True) -> str:
    r"""\
    >>> xmlformat('<?xml version="1.0"?><TEI></TEI>')
    '<?xml version="1.0" encoding="utf-8"?>\n<TEI />\n'

    >>> xmlformat('<editor><forename>Carmen Fotescu</forename><surname>Tauwinkl</surname></editor>', header=False)
    '<editor>\n    <forename>...</surname>\n</editor>\n'

    # invalid xml
    >>> xmlformat('<biblStruct type="bookSectionttp://zotero.org/groups/4545590/items/XN85KQZD">')
    Traceback (most recent call last):
    ...
    ValueError: invalid xml: no element found: line 1, column 77
     "<biblStruct type="bookSectionttp://zotero.org/groups/4545590/items/XN85KQZD">"
    >>> xmlformat('<biblStruct type="bookSection" xml:id="Hovhanessian2013">ABC</biblStruct>', header=False)
    '<biblStruct\n    xml:id="Hovhanessian2013"\n    type="bookSection"\n>\n    ABC\n</biblStruct>\n'
    """
    register_ns(source)
    raw = flat(source)
    parsed = cobdh.xml.parser.parse(raw)
    result = to_str(parsed, header)
    return result


def to_str(parsed, header: bool = False):
    formatted = ET.tostring(
        parsed,
        encoding='unicode',
        xml_declaration='utf8',
        method='cobdh',
    )
    if not header:
        result = formatted
    else:
        result = f'{HEADER}\n{formatted}'
    return result


def flat(source: str) -> str:
    try:
        parsed = ET.fromstring(
            source,
            parser=cobdh.xml.parser.parser_create(),
        )
    except ET.ParseError as error:
        raise ValueError(f'invalid xml: {error}\n "{source}"') from error
    ET.indent(parsed, space='')
    result = ET.tostring(
        parsed,
        encoding='unicode',
        xml_declaration='utf8',
    )
    result = '\n'.join(item.lstrip() for item in result.splitlines())
    result = result.replace('>\n<', '><')
    # avoid multiple white spaces inside long text strings.
    # normalize white spaces
    result = re.sub(
        r'[ ]+',
        ' ',
        result,
    )
    return result


NAMESPACE = re.compile(
    r'xmlns[ ]{0,3}\=[\"\'](http.+)[\"\']',
    flags=re.VERBOSE | re.IGNORECASE,
)


def register_ns(content: str):
    """Detect namespace to avoid ns0 as default namespace."""
    # TODO: DETERMINE WHY
    matched = NAMESPACE.search(content)
    if not matched:
        # could not find any default namespace
        return
    ET.register_namespace('', matched[1])
