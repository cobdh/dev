import pytest

import cobdh


def test_enrich(without_header):
    src = without_header.tmpdir
    completed = cobdh.utils.run(f'cob_enrich {src}')
    enriched_count = completed.stdout.count('enrich:')
    expected = len(cobdh.file_list(src))
    assert enriched_count == expected


@pytest.fixture
def samples(without_header):
    cobdh.utils.run(f'cob_enrich {without_header.tmpdir}')
    return without_header
