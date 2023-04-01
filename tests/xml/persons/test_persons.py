import collections

import cobdh
import cobdh.xmlx.enrich
import cobdh.xmlx.persons
import tests
import tests.xml.persons

EXPECTED = collections.OrderedDict([
    (
        'HovhanessianVahan',
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Hovhanessian',),
                forename=('Vahan',),
                lang='en',
            ),
        ]),
    ),
    (
        'MuyldermansJoseph',
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Muyldermans',),
                forename=('Joseph',),
                lang='en',
            ),
        ]),
    ),
    (
        'TakahashiHidemi',
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Takahashi',),
                forename=('Hidemi',),
                lang='en',
            ),
        ]),
    ),
    (
        'SemmelFranck',
        cobdh.Person(names=[
            cobdh.Name(
                surname=('Semmel',),
                forename=('Franck',),
                lang='en',
            ),
        ]),
    ),
])


def test_persons(samples):
    src = samples.tmpdir
    persons = cobdh.xmlx.persons.create(src)
    assert persons == EXPECTED


def test_inject_author_id():
    expected = 'xml:id="HilkensFranckAndy"'
    assert expected not in tests.xml.persons.PERSONS
    injected = cobdh.xmlx.enrich.inject_author_id(tests.xml.persons.PERSONS)
    assert expected in injected
    # ensure that multiple runs does not change the result
    again = cobdh.xmlx.enrich.inject_author_id(injected)
    assert again == injected


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
