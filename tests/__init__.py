import os

import cobdh

TESTS = os.path.join(cobdh.ROOT, 'tests')
PERSONS = os.path.join(TESTS, 'xml/data/persons')
assert os.path.exists(PERSONS)
