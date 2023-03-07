import collections

import cobdh.xml.persons

PERSONS = """\
<tei:TEI
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xml:lang="en"
>
    <analytic>
        <title level="a">
            An Armenian Invocational Prayer of a Lost Memra of Jacob of Serugh on Good
            Friday and the Destruction of Sheol
        </title>
        <tei:author>
            <tei:forename>Franck</tei:forename>
            <tei:forename>Andy</tei:forename>
            <tei:surname>Hilkens</tei:surname>
        </tei:author>
    </analytic>
</tei:TEI>
"""


def test_parse():
    expected = [
        (('Hilkens',), ('Franck', 'Andy')),
    ]
    parsed = cobdh.xml.persons.parse(PERSONS)
    assert parsed == expected


EXPECTED = collections.OrderedDict([
    ('Hovhanessian Vahan', (('Hovhanessian',), ('Vahan',))),
    ('Muyldermans Joseph', (('Muyldermans',), ('Joseph',))),
    ('Takahashi Hidemi', (('Takahashi',), ('Hidemi',))),
    ('Semmel Franck', (('Semmel',), ('Franck',)))
])


def test_persons(samples):
    src = samples.tmpdir
    persons = cobdh.xml.persons.create(src)
    assert persons == EXPECTED
