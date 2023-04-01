import cobdh.str

XML_ID = '{http://www.w3.org/XML/1998/namespace}id'
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'


def clean_id(xml: str):
    """\
    >>> clean_id('Ter-Girgorian ABC')
    'TerGirgorianABC'
    """
    for char in '.-:,;? ':
        xml = xml.replace(char, '')
    xml = cobdh.str.replace(xml)
    return xml
