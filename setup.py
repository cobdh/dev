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
    ],
    entry_points={
        'console_scripts': ['cob_xml = cobdh.cob_xml:main'],
    },
)
