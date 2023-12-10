import textwrap

import pytest

from enums import WriteOffType
from tests.factories import WriteOffFactory
from views import render_write_off


@pytest.mark.parametrize(
    'write_off_type, expected_write_off_type_name',
    (
            (
                    WriteOffType.EXPIRE_AT_15_MINUTES,
                    'Списание ингредиентов через 15 минут',
            ),
            (
                    WriteOffType.EXPIRE_AT_10_MINUTES,
                    'Списание ингредиентов через 10 минут',
            ),
            (
                    WriteOffType.EXPIRE_AT_5_MINUTES,
                    'Списание ингредиентов через 5 минут',
            ),
            (
                    WriteOffType.ALREADY_EXPIRED,
                    'В пиццерии просрочка',
            ),
    ),
)
def test_render_write_off(write_off_type, expected_write_off_type_name):
    write_off = WriteOffFactory(type=write_off_type)

    actual = render_write_off(write_off)
    expected = textwrap.dedent(f"""\
        <b>❗️ {write_off.unit_name} ❗️</b>
        {expected_write_off_type_name}""")

    assert actual == expected
