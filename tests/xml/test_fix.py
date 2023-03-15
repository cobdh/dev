import os

import cobdh
import cobdh.xmlx.fix
import tests

XML_DATA_BIBL = os.path.join(tests.TESTS, 'xml/data')


def test_fix_xml_id(testdir):
    src = XML_DATA_BIBL
    dst = testdir.tmpdir
    cobdh.xmlx.fix.xml_ids(src, dst)
    expected = 2
    current = len(cobdh.file_list(dst))
    assert current == expected
