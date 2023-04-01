import cobdh


def improve_name(person: tuple, log: bool = True) -> str:
    """\
    >>> improve_name(('Hovhanessian Vahan', (('Hovhanessian',), ('Vahan A. B.', ))))
    <BLANKLINE>
    before: ('Hovhanessian',) ('Vahan A. B.',)
    improved: ('Hovhanessian',) ('Vahan', 'A.', 'B.')
    ('Hovhanessian Vahan', (('Hovhanessian',), ('Vahan', 'A.', 'B.')))
    """
    assert isinstance(person, tuple), f'invalid input: {person} {type(person)}'
    forename = []
    for item in person[1][1]:
        forename.extend(item.split())
    surname = []
    for item in person[1][0]:
        surname.extend(item.split())
    result = (person[0], (tuple(surname), tuple(forename)))
    if log and result != person:
        cobdh.scribe(f'\nbefore: {person[1][0]} {person[1][1]}')
        cobdh.scribe(f'improved: {result[1][0]} {result[1][1]}')
    return result


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
