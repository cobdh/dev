import cobdh.xml.parser


def split(content: str, node: str) -> list:
    parsed = cobdh.xml.parser.parse(content)
    result = []
    for item in parsed.findall(node):
        result.append(item)
    return result
