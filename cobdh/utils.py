import os
import pathlib
import subprocess

SUCCESS = 0
FAILURE = 1
NEWLINE = '\n'


def file_read(path: str) -> str:
    """\
    >>> file_read(__file__)
    '...'
    """
    assert os.path.exists(path), str(path)
    with open(path, mode='r', encoding='utf8', newline=NEWLINE) as fp:
        return fp.read()


def file_replace(path: str, content='') -> str:
    content = content.rstrip() + NEWLINE
    with open(path, mode='w', encoding='utf8', newline=NEWLINE) as fp:
        fp.write(content)


def file_create(path: str, content='') -> str:
    assert not os.path.exists(path), f'already exists: {path}'
    content = content.rstrip() + NEWLINE
    with open(path, mode='w', encoding='utf8', newline=NEWLINE) as fp:
        fp.write(content)


def file_list(path: str) -> list:
    """\
    >>> file_list('.')
    [...]
    """
    path = pathlib.Path(path)
    result = list(path.glob('*'))
    return result


def run(cmd: str, cwd: str = None, expect=True):
    """\
    >>> run('ls')
    CompletedProcess(args=['ls'], returncode=0, stdout='...', stderr='')
    """
    cmd = cmd.split()
    cwd = cwd if cwd else os.getcwd()
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        check=False,
        encoding='utf8',
        universal_newlines=True,
    )
    if expect:
        assert completed.returncode == SUCCESS
    elif expect is False:  # pylint:disable=compare-to-zero
        assert completed.returncode >= FAILURE
    return completed
