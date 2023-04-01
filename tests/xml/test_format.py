import cobdh
import cobdh.xmlx.inter

SAMPLE = """\
<?xml version="1.0" encoding="utf-8"?>
<TEI xml:lang="de">
    <listBibl>
        <biblStruct
            corresp="http://zotero.org/groups/4545590/items/XN85KQZD"
            xml:id="Hovhanessian2013"
            type="bookSection"
        >
            <analytic>
                <title level="a">
                    <hi rend="italics">
                        Questions of the Queen of Sheba and Answers by King Solomon
                    </hi>
                    : Introduction and a New Translation of the Armenian Version
                </title>
                <author>
                    <forename>Vahan</forename>
                    <surname>Hovhanessian</surname>
                </author>
            </analytic>
        </biblStruct>
    </listBibl>
</TEI>
"""


def test_xmlformat():
    formatted = cobdh.xmlx.inter.xmlformat(SAMPLE)
    assert formatted == SAMPLE, formatted
    formatted = cobdh.xmlx.inter.xmlformat(formatted)


def test_multiple_xmlformat():
    formatted = SAMPLE
    # format ten time
    for _ in range(10):
        formatted = cobdh.xmlx.inter.xmlformat(formatted)
    assert formatted == SAMPLE


NAMESPACE = """\
<?xml version="1.0" encoding="utf-8"?>
<tei:TEI
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xml:lang="en"
>
    <tei:teiHeader>
        <tei:fileDesc>
            <!--hell-->
            <tei:titleStmt>
                <tei:editor
                    ref="https://cobdh.org/editors/schewe_helmut_konrad"
                    role="creator"
                />
            </tei:titleStmt>
        </tei:fileDesc>
    </tei:teiHeader>
</tei:TEI>
"""


def test_namespace():
    formatted = cobdh.xmlx.inter.xmlformat(NAMESPACE)
    assert formatted == NAMESPACE, formatted


SHORT = """\
<?xml version="1.0" encoding="utf-8"?>
<catalogue xml:lang="de">
    <msg key="bibl_bibliography">Bibliographie</msg>
    <msg key="bibl_record">Bibliographie-Eintrag</msg>
</catalogue>
"""


def test_single_short():
    formatted = cobdh.xmlx.inter.xmlformat(SHORT)
    assert formatted == SHORT, formatted


def test_cli_format(testdir):
    xml = testdir.tmpdir.join('abc.xml')
    cobdh.file_create(xml, NAMESPACE)
    completed = cobdh.utils.run('cob_xml .')
    # already well formatted
    assert 'skip: abc.xml' in completed.stdout
    # create bad formatted file
    cobdh.file_replace(xml, NAMESPACE.replace('   ', ''))
    completed = cobdh.utils.run('cob_xml .')
    # already well formatted
    assert 'format: abc.xml' in completed.stdout
    # format well formatted file, nothing todo
    completed = cobdh.utils.run('cob_xml .')
    assert 'skip: abc.xml' in completed.stdout


NS_META = """\
<?xml version="1.0" encoding="utf-8"?>
<meta xmlns="http://exist-db.org/xquery/repo">
    <description>TEI data used by cobdh-app</description>
    <author>cobdh.org</author>
    <website>http://cobdh.org/</website>
    <status>alpha</status>
    <license>GNU-LGPL</license>
    <copyright>true</copyright>
    <type>application</type>
    <target>cobdh-data</target>
    <prepare>pre-install.xql</prepare>
    <finish>post-install.xql</finish>
    <deployed>2015-04-23T13:17:07.65-04:00</deployed>
</meta>
"""


def test_format_ns_meta():
    """Do not replace default namespace with ns0."""
    formatted = cobdh.xmlx.inter.xmlformat(NS_META)
    assert formatted == NS_META, formatted


MULTIPLE_NAMESPACES = """\
<?xml version="1.0" encoding="utf-8"?>
<html
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:i18n="http://exist-db.org/xquery/i18n"
    data-template="app:determine_resource"
>
    <i18n:p/>
</html>
"""


def test_multiple_ns():
    formatted = cobdh.xmlx.inter.xmlformat(MULTIPLE_NAMESPACES)
    assert formatted == MULTIPLE_NAMESPACES, formatted


XSL = """\
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="2.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
>
    <xsl:template match="/">
        <ul>
            <xsl:for-each select="//tei:biblFull">
                <li>
                    <!--Example: cobdh.org/bibl/1-->
                    <xsl:element name="a">
                        <xsl:attribute name="href">
                            <!--TODO: REPLACE WITH app:abspath-->
                            <xsl:sequence select="concat('/exist/apps/cobdh-data/', 'bibl/', @xml:id)"/>
                        </xsl:attribute>
                        <xsl:value-of select=".//tei:title"/>
                        ;
                        <xsl:value-of select=".//tei:date"/>
                    </xsl:element>
                </li>
            </xsl:for-each>
        </ul>
    </xsl:template>
</xsl:stylesheet>
"""


def test_format_xsl():
    formatted = cobdh.xmlx.inter.xmlformat(XSL)
    cobdh.scribe(formatted)
    assert formatted == XSL, formatted
