from models import WriteOffType, WriteOff

__all__ = ('render_write_off',)

write_off_event_types_map = {
    WriteOffType.EXPIRE_AT_15_MINUTES: 'Списание ингредиентов через 15 минут',
    WriteOffType.EXPIRE_AT_10_MINUTES: 'Списание ингредиентов через 10 минут',
    WriteOffType.EXPIRE_AT_5_MINUTES: 'Списание ингредиентов через 5 минут',
    WriteOffType.ALREADY_EXPIRED: 'В пиццерии просрочка',
}


def render_write_off(write_off: WriteOff) -> str:
    write_off_type_name = write_off_event_types_map[write_off.type]
    return (
        f'<b>❗️ {write_off.unit_name} ❗️</b>\n'
        f'{write_off_type_name}'
    )
