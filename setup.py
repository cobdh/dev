import os
import re

import setuptools

ROOT = os.path.dirname(__file__)

with open(os.path.join(ROOT, 'cobdh/__init__.py'), encoding='utf8') as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

setuptools.setup(
    author='Helmut Konrad Schewe',
    author_email='helmutus@outlook.com',
    name='cob_dev',
    platforms='any',
    version=VERSION,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=[
        'cobdh',
        'cobdh.cli',
        'cobdh.xmlx',
        'cobdh.xmlx.persons',
        'cobdh.xmlx.validate',
    ],
    entry_points={
        'console_scripts': [
            'cob_bibl = cobdh.cli.bibl:main',
            'cob_enrich = cobdh.cli.enrich:main',
            'cob_persons = cobdh.cli.persons:main',
            'cob_split = cobdh.cli.split:main',
            'cob_validate = cobdh.cli.validate:main',
            'cob_xml = cobdh.cli.format:main',
        ],
    },
)
