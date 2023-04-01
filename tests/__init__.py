import os

import cobdh

TESTS = os.path.join(cobdh.ROOT, 'tests')
PERSONS = os.path.join(TESTS, 'xml/data/persons')
assert os.path.exists(PERSONS)
BIBL = os.path.join(TESTS, 'xml/data/bibl')
assert os.path.exists(BIBL)
