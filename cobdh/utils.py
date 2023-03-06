import os

SUCCESS = 0
FAILURE = 1


def file_read(path: str) -> str:
    """\
    >>> file_read(__file__)
    '...'
    """
    with open(path, mode='r', encoding='utf8', newline='\n') as fp:
        return fp.read()


def file_replace(path: str, content='') -> str:
    content = content.rstrip() + '\n'
    with open(path, mode='w', encoding='utf8', newline='\n') as fp:
        fp.write(content)


def file_create(path: str, content='') -> str:
    assert not os.path.exists(path), f'already exists: {path}'
    content = content.rstrip() + '\n'
    with open(path, mode='w', encoding='utf8', newline='\n') as fp:
        fp.write(content)
