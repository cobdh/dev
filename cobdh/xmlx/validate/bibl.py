import collections

import cobdh
import cobdh.xmlx
import cobdh.xmlx.fix


def validate(path: str):
    parsed = bibl_list(path)
    for key, value in parsed.items():
        if len(value) == 1:
            # expect unique xml id
            continue
        cobdh.error(f'duplicated xml id: {key}')
        cobdh.error(str(value))
        cobdh.scribe()


def bibl_list(src: str) -> dict:
    result = collections.defaultdict(set)
    for path in cobdh.file_list(src):
        content = cobdh.file_read(path)
        xmlid = parse_xmlid(content, path)
        if not xmlid:
            cobdh.error(f'invalid xmlid: {path}')
            continue
        result[xmlid].add(path)
    return result


def parse_xmlid(content: str, path: str = None):
    bibl = cobdh.xmlx.fix.parse(content)
    if bibl is None:
        cobdh.error(f'could not find bibl {path}')
        return None
    bibl = bibl[0]
    xmlid = bibl.attrib.get(
        cobdh.xmlx.XML_ID,
        False,
    )
    if not xmlid:
        cobdh.error(f'could not find @xml:id {path}')
        return None
    return xmlid
