import random

import cobdh
import cobdh.xmlx
import cobdh.xmlx.inter


def xml_ids(src: str, dst: str) -> dict:
    done = set()
    sources = cobdh.file_list(src)
    for path in sources:
        content = cobdh.file_read(path)
        try:
            improved = improve_xmlid_person(content, done)
        except ValueError:
            cobdh.error(f'could not parse: {path}')
            continue
        if not improved:
            continue
        fname = cobdh.file_name(path, ext=True)
        outpath = cobdh.join(dst, fname)
        cobdh.scribe(f'replace: {outpath}\n')
        cobdh.file_replace(outpath, improved)


def improve_xmlid_person(content: str, done: str) -> str:
    # do not expand namespaces
    cobdh.xmlx.inter.register_ns(content)  # TODO: REMOVE THIS
    parsed = parse(content)
    if parsed is None:
        raise ValueError('Could not parse')
    detected, root = parsed
    xmlid = NewBiblId(root, detected, done)()
    if xmlid is True:
        # nothing todo
        done.add(detected.attrib[cobdh.xmlx.XML_ID])
        return None
    done.add(xmlid)
    detected.attrib[cobdh.xmlx.XML_ID] = xmlid
    # convert node to xml
    result = cobdh.xml_tostr(
        root,
        header=True,
    )
    result = cobdh.xml_format(
        result,
        header=True,
    )
    return result


class NewBiblId:
    """Determine new xml-id for bibl items.

    If given id does not match requirements or are not unique in hole
    collection.
    """

    def __init__(self, root, content, done):
        self.root = root
        self.content = content
        self.done = done
        self.xmlid = content.attrib.get(cobdh.xmlx.XML_ID, '')

    def __call__(self):
        if self.valid:
            # nothing todo
            return True
        if self.empty:
            cobdh.scribe(f'create xml_id from nothing: {self.xmlid}')
            return self.new_from_empty()
        cobdh.scribe(f'duplicated xml_id: {self.xmlid}')
        result = self.new_from_current()
        cobdh.scribe(f'new xml_id: {result}')
        return result

    def new_from_current(self):
        new = cobdh.xmlx.clean_id(self.xmlid)
        for _ in range(20):
            new = nextid(new, self.done)
            if new not in self.done:
                return new
        # could not find a valid id
        assert 0, f'should not happen: {self.root}'

    def new_from_empty(self):
        new = create_id(self.root)
        if new not in self.done:
            return new
        for _ in range(20):
            new = nextid(new, self.done)
            if new not in self.done:
                return new
        # could not find a valid id
        assert 0, f'should not happen: {self.root}'

    @property
    def empty(self):
        cleaned = cobdh.xmlx.clean_id(self.xmlid)
        return not cleaned

    @property
    def valid(self):
        if not self.xmlid.strip():
            return False
        cleaned = cobdh.xmlx.clean_id(self.xmlid)
        if cleaned != self.xmlid:
            return False
        if self.xmlid in self.done:
            return False
        return True


def create_id(node) -> str:
    try:
        year = node.find('.//tei:body//tei:date', namespaces=cobdh.xmlx.NS).text
    except AttributeError:
        year = 'YYYY'
    try:
        name = node.find(
            './/tei:body//tei:surname',
            namespaces=cobdh.xmlx.NS,
        ).text
    except AttributeError:
        name = 'NONAME'
    result = f'{name}{year}'
    return result


def cleanup_id(node):
    """Remove danger elements `-:;` out of element identifier."""
    xmlid = node.attrib[cobdh.xmlx.XML_ID]
    cleaned = cobdh.xmlx.clean_id(xmlid)
    if xmlid == cleaned:
        return None
    node.attrib[cobdh.xmlx.XML_ID] = cleaned
    return node


def nextid(current: str, done: set):
    new = current + '_' + str(random.randint(1, 99))  # nosec
    if new in done:
        return nextid(new, done)
    return new


def parse(content: str):
    try:
        parsed = cobdh.xmlx.parser.parse(content)
    except ValueError:
        return None
    for item in './/tei:biblStruct .//tei:biblFull'.split():
        detected = parsed.find(item, namespaces=cobdh.xmlx.NS)
        if detected:
            return detected, parsed
    return None
