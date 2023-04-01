import cobdh
import cobdh.xmlx.fix
import tests

XML_DATA_BIBL = cobdh.join(tests.TESTS, 'xml/data', exist=True)


def test_fix_duplicated_xml_id(testdir):
    src = XML_DATA_BIBL
    dst = testdir.tmpdir
    cobdh.xmlx.fix.xml_ids(src, dst)
    expected = 2
    current = len(cobdh.file_list(dst))
    assert current == expected


INVALID_XML_ID = """\
<?xml version="1.0" encoding="utf-8"?>
<TEI
    xmlns="http://www.tei-c.org/ns/1.0"
    xml:lang="en"
>
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <editor
                    xml:id="schewe_helmut_konrad"
                    ref="https://cobdh.org/editors/schewe_helmut_konrad"
                    role="creator"
                />
            </titleStmt>
        </fileDesc>
    </teiHeader>
    <body>
        <biblStruct
            corresp="http://zotero.org/groups/4545590/items/MY8B5V8R"
            xml:id="???"
            type="thesis"
        >
            <monogr>
                <title level="m">
                    Traders of the Pearl: Persian and Armenian Christians in South-East Asia
                </title>
                <author>
                    <forename>Brian Edric</forename>
                    <surname>Colless</surname>
                </author>
                <imprint>
                    <date>1979</date>
                    <note type="thesisType">Th.D. dissertation</note>
                </imprint>
            </monogr>
        </biblStruct>
    </body>
</TEI>
"""

NO_XML_ID = INVALID_XML_ID.replace('xml:id="???"', '')


def test_fix_invalid_xml_id():
    assert 'xml:id="???"' in INVALID_XML_ID
    improved = cobdh.xmlx.fix.improve_xmlid_person(
        INVALID_XML_ID,
        done=set(),
    )
    assert 'xml:id="Colless1979"' in improved


def test_fix_no_xml_id():
    improved = cobdh.xmlx.fix.improve_xmlid_person(
        NO_XML_ID,
        done=set(),
    )
    assert 'xml:id="Colless1979"' in improved


def test_cli_fix(samples):
    src = samples.tmpdir
    cobdh.run(f'cob_bibl {src}')
