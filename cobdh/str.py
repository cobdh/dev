import contextlib
import sys


def replace(*items):
    """Convert to ASCII.

    >>> replace('α', 'χ', '²', 'Abc')
    ['a', 'c', '2', 'Abc']
    >>> replace('Hαχ²')
    'Hac2'
    >>> replace('χ')
    'c'
    """
    result = []
    for item in items:
        replaced = []
        for char in item:
            with contextlib.suppress(KeyError):
                char = MATCHED[char]
            replaced.append(char)
        result.append(''.join(replaced))
    if len(result) == 1:
        return result[0]
    return result


def alphabetically(item: str) -> str:
    if item is None:
        # sort at the end, use max value
        return chr(0x10ffff)
    return replace(item).lower()


def fix_encoding(msg: str) -> str:
    """Remove invalid character to display on console

    Args:
        msg(str): message with invalid character
    Returns:
        message `without` invalid character
    """
    # ensure to have str
    msg = str(msg)
    # convert for windows console
    encoding = 'cp1252' if 'win' in sys.platform else 'utf-8'
    # remove non valid char to avoid errors on win-console
    msg = msg.encode(encoding, errors='xmlcharrefreplace').decode(encoding)
    return msg


def scribe(*msg: str, sep: str = ' ', end: str = '\n'):
    """Log safely to console.

    >>> scribe('Hello')
    Hello
    """
    msg = sep.join(msg)
    msg = fix_encoding(msg)
    print(
        msg,
        file=sys.stdout,
        end=end,
        flush=True,
    )


def error(*msg: str, sep: str = ' ', end: str = '\n'):
    """Log error safely to stderr."""
    msg = sep.join(msg)
    msg = f'[ERROR]: {msg}'
    msg = fix_encoding(msg)
    print(
        msg,
        file=sys.stderr,
        end=end,
        flush=True,
    )


TABLE = """\
α           a
β           b
γ           g
δ           d
ε           ep
ζ           z
η           et
θ           t
ι           i
κ           k
λ           l
μ           m
ν           n
ξ           x
π           pi
ρ           r
σ           s
τ           t
υ           up
φ           phi
χ           c
ψ           psi
ω           o
Γ           G
Δ           E
Θ           T
Λ           L
Ξ           X
Π           PI
Σ           SI
Υ           UP
Φ           PH
Ψ           PS
Ω           OM
⁰           0
¹           1
²           2
³           3
⁴           4
⁵           5
⁶           6
⁷           7
⁸           8
⁹           9
₀           0
₁           1
₂           2
₃           3
₄           4
₅           5
₆           6
₇           7
₈           8
₉           9
ä           ae
ö           oe
ü           ue
Ä           AE
Ö           OE
Ü           UE
ß           ss
"""
# TODO: REPLACE WITH SHARK OPERATOR, PYTHON 3.8
MATCHED = {
    item.split()[0]: item.split()[1] for item in TABLE.strip().splitlines()
}
