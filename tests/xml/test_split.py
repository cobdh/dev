import os

import pytest

import cobdh
import cobdh.cli.split
import cobdh.xml.inter

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
                <author>
                    <forename>Franck</forename>
                    <surname>Semmel</surname>
                </author>
            </analytic>
            <series>
                <title level="s">Eastern Christian Studies 9</title>
            </series>
        </biblStruct>
    </listBibl>
</TEI>
"""


@pytest.fixture
def without_header(testdir):
    path = testdir.tmpdir.join('data.xml')
    cobdh.file_create(path, SAMPLE)
    current = len(cobdh.file_list(testdir.tmpdir))
    assert current == 1, current
    cmd = f'cob_split --src {path} --node .//biblStruct --index 10'
    cobdh.utils.run(cmd, cwd=testdir.tmpdir)
    os.unlink(path)
    return testdir


def test_splitby_biblstruct():
    expected = 3
    result = cobdh.cli.split.split(SAMPLE, node='.//biblStruct')
    assert len(result) == expected


def test_cli_splitby(testdir):
    path = testdir.tmpdir.join('data.xml')
    cobdh.file_create(path, SAMPLE)
    current = len(cobdh.file_list(testdir.tmpdir))
    assert current == 1, current
    cmd = f'cob_split --src {path} --node .//biblStruct --index 10'
    completed = cobdh.utils.run(cmd, cwd=testdir.tmpdir)
    assert '10:' in completed.stdout
    assert '11:' in completed.stdout
    assert '12:' in completed.stdout
    current = len(cobdh.file_list(testdir.tmpdir))
    assert current == 4, current
