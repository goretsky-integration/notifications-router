import factory

__all__ = (
    'generate_order_number',
    'generate_unit_name',
)


def generate_unit_name() -> str:
    return f'Москва 4-{factory.Faker("random_int", min=1, max=100)}'


def generate_order_number() -> str:
    return (
        f'{factory.Faker("random_int")}'
        f'-{factory.Faker("random_int", min=1, max=1000)}'
    )
