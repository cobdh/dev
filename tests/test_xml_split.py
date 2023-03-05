import cobdh.xml.inter
import cobdh.xml.split

SAMPLE = """\
<?xml version="1.0" encoding="UTF-8"?>
<TEI>
    <listBibl>
        <biblStruct
            type="bookSection"
            xml:id="Hovhanessian2013"
            corresp="http://zotero.org/groups/4545590/items/XN85KQZD">
            <analytic>
                <title level="a">
                    <hi rend="italics">Questions of the Queen of Sheba and Answers by King Solomon</hi>:
                    Introduction and a New Translation of the Armenian Version </title>
                <author>
                    <forename>Vahan</forename>
                    <surname>Hovhanessian</surname>
                </author>
            </analytic>
        </biblStruct>
        <biblStruct
            type="journalArticle"
            xml:id="Muyldermans1946"
            corresp="http://zotero.org/groups/4545590/items/4UIY4CZJ">
            <analytic>
                <title level="a">
                    <hi rend="italics">Sur les Séraphins</hi> et <hi rend="italics">Sur les
                        Chérubins</hi> d’Évagre le Pontique dans les versions syriaque et arménienne </title>
                <author>
                    <forename>Joseph</forename>
                    <surname>Muyldermans</surname>
                </author>
            </analytic>
        </biblStruct>
        <biblStruct
            type="bookSection"
            xml:id="Takahashi2010"
            corresp="http://zotero.org/groups/4545590/items/G7NVVB94">
            <analytic>
                <title level="a"> A <hi rend="italics">Mimro </hi>on Maphrian Gregory Barṣawmo Ṣafī
                    Bar ‘Ebroyo by Dioscorus Gabriel of Barṭelli, Bishop of Gozarto d-Qardu </title>
                <author>
                    <forename>Hidemi</forename>
                    <surname>Takahashi</surname>
                </author>
            </analytic>
            <series>
                <title level="s">Eastern Christian Studies 9</title>
            </series>
        </biblStruct>
    </listBibl>
</TEI>
"""


def test_splitby_biblstruct():
    expected = 3
    result = cobdh.xml.split.split(SAMPLE, node='.//biblStruct')
    assert len(result) == expected
