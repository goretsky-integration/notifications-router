import factory.fuzzy

from models import WriteOff
from enums import WriteOffType

__all__ = ('WriteOffFactory',)


class WriteOffFactory(factory.Factory):
    class Meta:
        model = WriteOff

    unit_name = factory.Sequence(lambda n: f'Москва-{n}')
    type = factory.fuzzy.FuzzyChoice(WriteOffType)
