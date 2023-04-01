import collections
import os

import cobdh
import cobdh.xmlx.enrich
import cobdh.xmlx.persons
import cobdh.xmlx.persons.parser
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
    parsed = cobdh.xmlx.persons.parser.parse(PERSONS)
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


def test_persons_list():
    listed = cobdh.xmlx.persons.persons_list(tests.PERSONS)
    assert len(listed) == 2
    assert 'HovhanessianVahan' in listed
    assert 'Ovid44' in listed


def test_persons_cli(testdir):
    src = tests.BIBL
    cobdh.run(f'cob_persons {src}')
    expected = 6
    persons = cobdh.file_list(path=testdir.tmpdir)
    assert len(persons) >= expected


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
