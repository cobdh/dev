import os

import cobdh

TESTS = cobdh.join(cobdh.ROOT, 'tests', exist=True)
PERSONS = cobdh.join(TESTS, 'xml/data/persons', exist=True)
BIBL = cobdh.join(TESTS, 'xml/data/bibl', exist=True)
