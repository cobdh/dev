import cobdh
import cobdh.xmlx.persons.parser
import tests
import tests.xml.persons


def test_parse():
    expected = [
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Hilkens',),
                forename=('Franck', 'Andy'),
                lang='en',
            )
        ]),
    ]
    parsed = cobdh.xmlx.persons.parser.parse(tests.xml.persons.PERSONS)
    assert parsed == expected


def test_parse_idem():
    path = cobdh.join(tests.TESTS, 'xml/data/idem.xml', exist=True)
    content = cobdh.file_read(path)
    expected = [
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Macler',),
                forename=('Frédéric',),
                lang='en',
            ),
        ]),
        cobdh.Person(
            names=[cobdh.Name(
                surname=('Idem',),
                forename=[],
                lang='en',
            )]),
    ]
    parsed = cobdh.xmlx.persons.parser.parse(content)
    assert parsed == expected


def test_parse_author_raw():
    path = cobdh.join(tests.TESTS, 'xml/data/bibl/1.xml', exist=True)
    content = cobdh.file_read(path)
    expected = [
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Blain',),
                forename=('Virginia',),
                lang='en',
            )
        ],),
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Clements',),
                forename=('Patricia',),
                lang='en',
            )
        ]),
    ]
    parsed = cobdh.xmlx.persons.parser.parse(content)
    assert parsed == expected


def test_arabic():
    src = cobdh.join(tests.BIBL, '2.xml', exist=True)
    content = cobdh.file_read(src)
    parsed = cobdh.xmlx.persons.parser.parse(content)
    expected = [
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Barsoum',),
                forename=('Ignatius', 'Afram'),
                lang='en',
            ),
            cobdh.Name(
                surname=('\u0628\u0631\u0635\u0648\u0645',),
                forename=(
                    '\u0627\u063a\u0646\u0627\u0637\u064a\u0648\u0633',
                    '\u0627\u0641\u0631\u0627\u0645',
                ),
                lang='ar',
            ),
        ]),
    ]
    assert parsed == expected
