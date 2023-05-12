import cobdh
import tests


def test_cli_validate_persons():
    src = tests.DATA
    completed = cobdh.run(f'cob_validate {src}')
    stderr = completed.stderr
    counted = stderr.count('no persons')
    assert counted == 2
