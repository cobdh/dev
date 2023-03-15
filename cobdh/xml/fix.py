import os
import random

import cobdh
import cobdh.xml.inter

XML_ID = '{http://www.w3.org/XML/1998/namespace}id'


def xml_id(src: str, dst: str) -> dict:
    done = set()
    sources = cobdh.file_list(src)
    for path in sources:
        content = cobdh.file_read(path)
        # do not expand namespaces
        cobdh.xml.inter.register_ns(content)  # TODO: REMOVE THIS
        parsed = parse(content)
        if parsed is None:
            print(f'[ERROR]: could not parse: {path}')
            continue
        detected, root = parsed
        # TODO: XML:ID
        xmlid = detected.attrib[XML_ID]
        if xmlid not in done:
            done.add(xmlid)
            continue
        print(f'duplicated xmlid: {xmlid}')
        newid = nextid(xmlid, done=done)
        print(f'use new id: {newid}')
        detected.attrib[XML_ID] = newid
        fname = cobdh.file_name(path, ext=True)
        outpath = cobdh.forward_slash(os.path.join(dst, fname))
        print(f'replace: {outpath}\n')
        formatted = cobdh.xml_tostr(
            root,
            header=True,
        )
        cobdh.file_replace(outpath, formatted)


def nextid(current: str, done: set):
    new = current + '_' + str(random.randint(1, 99))  # nosec
    if new in done:
        return nextid(new, done)
    return new


NS = {
    'tei': 'http://www.tei-c.org/ns/1.0',
}


def parse(content: str):
    try:
        parsed = cobdh.xml.parser.parse(content)
    except ValueError:
        return None
    for item in './/tei:biblStruct .//tei:biblFull'.split():
        detected = parsed.find(item, namespaces=NS)
        if detected:
            return detected, parsed
    return None
