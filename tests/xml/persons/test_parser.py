import os

import cobdh
import cobdh.xmlx.persons.parser
import tests
import tests.xml.persons


def test_parse():
    expected = [
        (('Hilkens',), ('Franck', 'Andy')),
    ]
    parsed = cobdh.xmlx.persons.parser.parse(tests.xml.persons.PERSONS)
    assert parsed == expected


def test_parse_idem():
    path = os.path.join(tests.TESTS, 'xml/data/idem.xml')
    assert os.path.exists(path), path
    content = cobdh.file_read(path)
    expected = [
        (('Macler',), ('Frédéric',)),
        (('Idem',), ()),
    ]
    parsed = cobdh.xmlx.persons.parser.parse(content)
    assert parsed == expected


def test_parse_author_raw():
    path = os.path.join(tests.TESTS, 'xml/data/bibl/1.xml')
    assert os.path.exists(path), path
    content = cobdh.file_read(path)
    expected = [
        (('Blain',), ('Virginia',)),
        (('Clements',), ('Patricia',)),
    ]
    parsed = cobdh.xmlx.persons.parser.parse(content)
    assert parsed == expected


def test_arabic():
    src = os.path.join(tests.BIBL, '2.xml')
    content = cobdh.file_read(src)
    parsed = cobdh.xmlx.persons.parser.parse(content)
    expected = [
        (('Barsoum',), ('Ignatius', 'Afram')),
        (('\u0628\u0631\u0635\u0648\u0645',),
         ('\u0627\u063a\u0646\u0627\u0637\u064a\u0648\u0633',
          '\u0627\u0641\u0631\u0627\u0645')),
    ]
    assert parsed == expected
