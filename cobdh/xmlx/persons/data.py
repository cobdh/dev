"""\
>>> name = Name(surname=('Hovhanessian',), forename=('Vahan', 'A.', 'B.',))
>>> hov = Person([name])
>>> hov.xmlid
'HovhanessianVahanAB'
"""
import dataclasses

import cobdh.xmlx


@dataclasses.dataclass
class Name:
    surname: list = dataclasses.field(default_factory=list)
    forename: list = dataclasses.field(default_factory=list)
    lang: str = 'en'

    @property
    def xmlid(self):
        hashed = ' '.join(self.surname) + ' '
        hashed += ' '.join(self.forename)
        hashed: str = cobdh.xmlx.clean_id(hashed)
        return hashed


@dataclasses.dataclass
class Person:
    names: list = dataclasses.field(default_factory=list)

    @property
    def xmlid(self):
        # TODO: PREFERE LATIN XMLID
        return self.names[0].xmlid
