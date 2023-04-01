import contextlib
import os
import pathlib
import re
import subprocess

import cobdh

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


def file_list(
    path,
    exts: str = 'xml',
    sort: bool = True,
):
    """\
    >>> file_list('.', exts='*')
    [...]
    """
    path = pathlib.Path(path)
    result = [path]
    if not path.is_file():
        result = []
        for ext in exts.split():
            result += list(path.glob(f'**/*.{ext}'))
    if sort:
        result = files_sort(result)
    return result


def file_name(path: str, ext: bool = False) -> str:
    """Determine file name without file extension out of file path.

    >>> file_name('/etc/profile.d/helm.sh')
    'helm'
    >>> file_name('info.txt')
    'info'
    >>> file_name('/etc/.tmp')
    '.tmp'
    >>> file_name('.etc')
    '.etc'
    >>> file_name('/no/file/ext')
    'ext'
    >>> file_name('etc/dev/raw.png', ext=True)
    'raw.png'
    """
    assert path, path
    path = forward_slash(path)
    try:
        _, name = path.rsplit('/', 1)
    except ValueError:
        name = path
    if ext:
        return name
    if name[0] == '.':
        return name
    result = name.split('.')[0]
    return result


def files_sort(files: list) -> list:
    """Sort `files` path alphabetically. Sort file names by number if given.

    >>> files_sort(('/c/a', '/c/200.txt', '/c/2.txt', '/c/3', '/c/0.bmp'))
    ['/c/0.bmp', '/c/2.txt', '/c/3', '/c/200.txt', '/c/a']
    """
    files = [forward_slash(str(item)) for item in files]

    def number_filename(item):
        # sort file names if they are numbers: 0,1,2,3,4,5,6,7,8,9,10
        item = item.lower()
        item = file_name(item)
        with contextlib.suppress(ValueError):
            # sort items by number
            item = int(item)
            # ensure to compare str and str and not str and int
            item = str(item).zfill(20)
        return item

    files = sorted(files, key=number_filename)
    return files


BACKSLASH = re.compile(r'\\')
NL = re.compile(r'\\(?!n)')


def forward_slash(content: str, keep_newline: bool = False) -> str:
    r"""Replace every backward slash \\ with an forward slash /.

    Args:
        content(str): content with backslash's
        keep_newline(bool): if True, do not convert \n to /n
    Returns:
        content without backslash's

    Examples:
    >>> forward_slash('\\helm\nelm', keep_newline=True)
    '/helm\nelm'
    >>> forward_slash('\\helm\\telm', keep_newline=True)
    '/helm/telm'
    >>> forward_slash('\\helm\\nelm')
    '/helm/nelm'
    """
    assert isinstance(content, str), str(content)
    pattern = BACKSLASH
    if keep_newline:
        pattern = NL
    content = re.sub(pattern, '/', content)
    return content


def run(cmd: str, cwd: str = None, expect=True):
    """\
    >>> run('ls')
    CompletedProcess(args=['ls'], returncode=0, stdout='...', stderr='')
    """
    cmd = cmd.split()
    cwd = cwd if cwd else os.getcwd()
    completed = subprocess.run(  # nosec
        cmd,
        cwd=cwd,
        capture_output=True,
        check=False,
        encoding='utf8',
        universal_newlines=True,
    )
    if expect:
        if completed.returncode != SUCCESS:
            cobdh.scribe(completed.stdout)
            cobdh.error(completed.stderr)
        assert completed.returncode == SUCCESS
    elif expect is False:  # pylint:disable=compare-to-zero
        assert completed.returncode >= FAILURE, str(completed)
    return completed
