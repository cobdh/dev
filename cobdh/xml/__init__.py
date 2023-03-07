import cobdh.string


def clean_id(xml: str):
    """\
    >>> clean_id('Ter-Girgorian ABC')
    'TerGirgorianABC'
    """
    for char in '.-: ':
        xml = xml.replace(char, '')
    xml = cobdh.string.replace(xml)
    return xml
