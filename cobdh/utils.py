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
