#!/usr/bin/env python
import collections
import functools
import os
import re
import urllib.error
import urllib.parse
import urllib.request

import cobdh

# TODO: VERIFY DEFAULT VALUE
# front end
BASE = os.environ.get('SERVER_TEST', 'http://view/exist/apps/cobdh/')
BASE = BASE.rstrip('/')

# TODO: IMPROVE VIA GOOGLE
HREF = re.compile(r'a[ ]{1,4}href[ ]{0,4}=[ ]{0,4}[\"\'](.+?)[\"\']')


def urls(root: str = BASE, deep: int = 5) -> list:
    result = collections.defaultdict(set)
    result[root] = set()
    if deep < 0:
        return result
    try:
        content = curl(root)
    except urllib.error.HTTPError:
        cobdh.scribe(f'could not curl: {root}')
        result[root].add('[OFFLINE]')
        return result
    for hyperhyper in HREF.findall(content):
        if hyperhyper == '/':
            continue
        hyperhyper = url_fix(hyperhyper)
        hyperhyper = abspath(root, hyperhyper)
        if hyperhyper in result:
            result[hyperhyper].add(root.rstrip('/'))
            continue
        result[hyperhyper].add(root.rstrip('/'))
        children = urls(
            root=hyperhyper,
            deep=deep - 1,
        )
        for key, value in children.items():
            result[key] |= value
    return result


def url_fix(s):
    """Fixes URLs by quoting unsafe characters in the path."""
    scheme, netloc, path, query, fragment = urllib.parse.urlsplit(s)
    path = urllib.parse.quote(urllib.parse.unquote(path))
    result = urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))
    return result


def abspath(root, hyper):
    if urllib.parse.urlsplit(hyper).netloc:
        # already abspath
        return hyper
    hyper = hyper.strip()
    # ensure to start with /
    hyper = '/' + hyper.lstrip('/')
    # TODO: THERE MUST BE A BETTER WAY
    splitted = urllib.parse.urlsplit(root)
    root = splitted.scheme + '://' + splitted.netloc
    result = f'{root}{hyper}'
    return result


@functools.lru_cache(maxsize=2048)
def curl(path: str):
    url = url_fix(path)
    with urllib.request.urlopen(url) as response:  # nosec
        html = response.read()
    html: str = html.decode('utf8')
    return html


def main() -> int:
    result = urls(deep=5)
    cobdh.scribe()
    for key, value in result.items():
        cobdh.scribe(f'{key}\n\t{value}\n')
    return cobdh.SUCCESS


if __name__ == "__main__":
    main()
