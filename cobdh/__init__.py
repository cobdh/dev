import os

from cobdh.string import alphabetically
from cobdh.string import replace
from cobdh.utils import FAILURE
from cobdh.utils import NEWLINE
from cobdh.utils import SUCCESS
from cobdh.utils import file_create
from cobdh.utils import file_list
from cobdh.utils import file_name
from cobdh.utils import file_read
from cobdh.utils import file_replace
from cobdh.utils import files_sort
from cobdh.utils import forward_slash
from cobdh.utils import run
from cobdh.xml.inter import to_str as xml_tostr
from cobdh.xml.parser import parse as xml_parse

__version__ = '0.1.0'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
