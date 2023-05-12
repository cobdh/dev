import cobdh
import cobdh.xmlx.persons
import cobdh.xmlx.persons.parser


def validate(path: str):
    parsed = cobdh.xmlx.persons.persons_list(path)
    for key, value in parsed.items():
        cobdh.scribe(key)
        cobdh.scribe(value)
        content = cobdh.file_read(value)
        parsed = cobdh.xmlx.persons.parser.parse(content)
        if not parsed:
            cobdh.error('no persons')
        else:
            cobdh.scribe(parsed)
        print()
