from cobdh.xml.formatter import ET


def parse(raw: str):
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
