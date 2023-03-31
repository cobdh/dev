import collections
import os

import cobdh
import cobdh.xmlx.enrich
import cobdh.xmlx.persons
import tests

PERSONS = """\
<TEI
    xmlns="http://www.tei-c.org/ns/1.0"
    xml:lang="en"
>
    <analytic>
        <title level="a">
            An Armenian Invocational Prayer of a Lost Memra of Jacob of Serugh on Good
            Friday and the Destruction of Sheol
        </title>
        <author>
            <forename>Franck</forename>
            <forename>Andy</forename>
            <surname>Hilkens</surname>
        </author>
    </analytic>
</TEI>
"""


def test_parse():
    expected = [
        (('Hilkens',), ('Franck', 'Andy')),
    ]
    parsed = cobdh.xmlx.persons.parse(PERSONS)
    assert parsed == expected


EXPECTED = collections.OrderedDict([
    ('HovhanessianVahan', (('Hovhanessian',), ('Vahan',))),
    ('MuyldermansJoseph', (('Muyldermans',), ('Joseph',))),
    ('TakahashiHidemi', (('Takahashi',), ('Hidemi',))),
    ('SemmelFranck', (('Semmel',), ('Franck',)))
])


def test_persons(samples):
    src = samples.tmpdir
    persons = cobdh.xmlx.persons.create(src)
    assert persons == EXPECTED


def test_inject_author_id():
    expected = 'xml:id="HilkensFranckAndy"'
    assert expected not in PERSONS
    injected = cobdh.xmlx.enrich.inject_author_id(PERSONS)
    assert expected in injected
    # ensure that multiple runs does not change the result
    again = cobdh.xmlx.enrich.inject_author_id(injected)
    assert again == injected


def test_parse_idem():
    path = os.path.join(tests.TESTS, 'xml/data/idem.xml')
    assert os.path.exists(path), path
    content = cobdh.file_read(path)
    expected = [
        (('Macler',), ('Frédéric',)),
        (('Idem',), ()),
    ]
    parsed = cobdh.xmlx.persons.parse(content)
    assert parsed == expected


def test_parse_author_raw():
    path = os.path.join(tests.TESTS, 'xml/data/bibl/1.xml')
    assert os.path.exists(path), path
    content = cobdh.file_read(path)
    expected = [
        ('Blain, Virginia', ()),
        ('Clements, Patricia', ()),
    ]
    parsed = cobdh.xmlx.persons.parse(content)
    print(parsed)
    assert parsed == expected
