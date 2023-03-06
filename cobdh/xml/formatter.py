import textwrap
import xml.etree.ElementTree as ET

SHORT_ITEM_WIDTH_MAX = 40
# pylint:disable=C0103


def cobdh_xml(write, elem, qnames, namespaces, short_empty_elements, **kwargs):  # pylint:disable=R1260,R0914,R0915
    tag = elem.tag
    text = elem.text
    namespaces = namespaces if namespaces else {}
    level = kwargs.get('level', -1) + 1
    ident = level * 4 * ' '
    if tag is ET.Comment:
        write(ident + "<!--%s-->\n" % text.strip())
    elif tag is ET.ProcessingInstruction:  # pylint:disable=R1702
        write("<?%s?>\n" % text)
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(escape_cdata(text))
            for e in elem:
                cobdh_xml(
                    write,
                    e,
                    qnames,
                    None,
                    short_empty_elements=short_empty_elements,
                    level=level,
                )
        else:
            write(ident + "<" + tag)
            items = list(elem.items())
            items.sort(key=alphabetically_with_ns)
            numbers = len(items) + len(namespaces)
            if numbers > 1:
                write('\n')
            if numbers:
                index = 0
                after = '\n' if numbers > 1 else ''
                if namespaces:
                    before = ident + '   ' if index or numbers > 1 else ''
                    # sort on prefix
                    for v, k in sorted(namespaces.items(), key=lambda x: x[1]):
                        if k:
                            k = ":" + k
                        ns_item = " xmlns%s=\"%s\"" % (k, escape_attrib(v))
                        write(f'{before}{ns_item}{after}')
                        index += 1
                for k, v in items:
                    if isinstance(k, ET.QName):
                        k = k.text
                    if isinstance(v, ET.QName):
                        v = qnames[v.text]
                    else:
                        v = escape_attrib(v)
                    # do not add newline for last item
                    before = ident + '   ' if index or numbers > 1 else ''
                    value_item = " %s=\"%s\"" % (qnames[k], v)
                    write(f'{before}{value_item}{after}')
                    index += 1
            if text or len(elem) or not short_empty_elements:
                short = not len(elem)  # pylint:disable=C1802
                short = short and len(text.strip()) < SHORT_ITEM_WIDTH_MAX
                # do not shorten more than one attribute
                short = short and numbers <= 1
                if numbers <= 1:
                    # zero or one attribute
                    if short:
                        write(">")
                    else:
                        write(">\n")
                else:
                    write(ident + ">\n")
                if text:
                    if short:
                        line = text.strip()
                    else:
                        line = ident_text(text, ident + ' ' * 4)
                    write(line)
                for e in elem:
                    cobdh_xml(
                        write,
                        e,
                        qnames,
                        None,
                        short_empty_elements=short_empty_elements,
                        level=level,
                    )
                if short:
                    write("</" + tag + ">\n")
                else:
                    write(ident + "</" + tag + ">\n")
            else:
                if len(items) <= 1:  # pylint:disable=R5501
                    # zero or one attribute
                    write("/>\n")
                else:
                    write(ident + "/>\n")
    if elem.tail:
        indented = ident_text(elem.tail, ident)
        write(indented)


def ident_text(data, ident: str, textwidth_max: int = 80) -> str:
    r"""\
    >>> ident_text('\n\nHello\nABC\nDEF\n\n', '    ')
    '    Hello ABC DEF\n'
    """
    escaped = escape_cdata(data)
    escaped = escaped.strip()
    wrapped = textwrap.wrap(
        text=escaped,
        width=textwidth_max,
    )
    wrapped: str = '\n'.join(wrapped)
    indented = textwrap.indent(
        wrapped,
        ident,
    )
    result = indented
    # add final newline
    result += '\n'
    return result


def alphabetically_with_ns(item):
    """\
    >>> alphabetically_with_ns(('{http://www.w3.org/XML/1998/namespace}lang', 'en'))
    'lang'
    >>> alphabetically_with_ns(('lang', 'en'))
    'lang'
    """
    item = item[0]
    try:
        item = item.split('}')[1]
    except IndexError:
        pass
    return item


def escape_cdata(value):
    return ET._escape_cdata(value)  # pylint:disable=W0212


def escape_attrib(value):
    return ET._escape_attrib(value)  # pylint:disable=W0212


ET.register_namespace('tei', "http://www.tei-c.org/ns/1.0")

ET._serialize['cobdh'] = cobdh_xml  # pylint:disable=W0212
