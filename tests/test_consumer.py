import pytest

from consumer import bytes_to_dict


@pytest.mark.parametrize(
    'message_bytes,expected',
    [
        (b'{"hello": "world"}', {'hello': 'world'}),
        (b'{}', {}),
    ]
)
def test_bytes_to_dict(message_bytes, expected):
    assert bytes_to_dict(message_bytes) == expected
