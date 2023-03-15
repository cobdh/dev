import cobdh.str


def clean_id(xml: str):
    """\
    >>> clean_id('Ter-Girgorian ABC')
    'TerGirgorianABC'
    """
    for char in '.-:,; ':
        xml = xml.replace(char, '')
    xml = cobdh.str.replace(xml)
    return xml
