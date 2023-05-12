import os

import cobdh

TESTS = cobdh.join(cobdh.ROOT, 'tests', exist=True)
DATA = cobdh.join(TESTS, 'xml/data', exist=True)
PERSONS = cobdh.join(DATA, 'persons', exist=True)
BIBL = cobdh.join(DATA, 'bibl', exist=True)
