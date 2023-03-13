import collections

import cobdh.xml.persons

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
    parsed = cobdh.xml.persons.parse(PERSONS)
    assert parsed == expected


EXPECTED = collections.OrderedDict([
    ('HovhanessianVahan', (('Hovhanessian',), ('Vahan',))),
    ('MuyldermansJoseph', (('Muyldermans',), ('Joseph',))),
    ('TakahashiHidemi', (('Takahashi',), ('Hidemi',))),
    ('SemmelFranck', (('Semmel',), ('Franck',)))
])


def test_persons(samples):
    src = samples.tmpdir
    persons = cobdh.xml.persons.create(src)
    assert persons == EXPECTED
