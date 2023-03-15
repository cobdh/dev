import os

import cobdh
import cobdh.xml.fix
import tests

XML_DATA_BIBL = os.path.join(tests.TESTS, 'xml/data')


def test_fix_xml_id(testdir):
    src = XML_DATA_BIBL
    dst = testdir.tmpdir
    cobdh.xml.fix.xml_id(src, dst)
    expected = 2
    current = len(cobdh.file_list(dst))
    assert current == expected
