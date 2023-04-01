import cobdh


def improve_name(person: 'cobdh.Person', log: bool = True) -> str:
    """\
    >>> import cobdh;improve_name(cobdh.Person(names=[cobdh.Name(forename=('Hovhanessian',), surname=('Vahan A. B.', ))]))
    <BLANKLINE>
    before: ('Hovhanessian',) ('Vahan A. B.',)
    improved: ('Hovhanessian',) ('Vahan', 'A.', 'B.')
    Person(names=[Name(surname=('Vahan', 'A.', 'B.'), forename=('Hovhanessian',), lang='en')])
    """
    cobdh.asserts(person, cobdh.Person)
    for name in person.names:
        surname = []
        for item in name.surname:
            surname.extend(item.split())
        surname: tuple = tuple(surname)
        forename = []
        for item in name.forename:
            forename.extend(item.split())
        forename: tuple = tuple(forename)
        if log and surname != name.surname or forename != name.forename:
            cobdh.scribe(f'\nbefore: {name.forename} {name.surname}')
            cobdh.scribe(f'improved: {forename} {surname}')
        name.surname = surname
        name.forename = forename
    return person


def simple_name(name: str) -> tuple:
    """\
    >>> simple_name('Blain, Virginia')
    (('Blain',), ('Virginia',))
    """
    if ',' not in name:
        return None
    name = name.strip()
    first, second = name.split(',')
    result = tuple(first.split()), tuple(second.split())
    return result
