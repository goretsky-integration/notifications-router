from typing import Generator

CHUNK_SYMBOLS_COUNT = 4096


def get_text_by_chunks(text: str) -> Generator[str, None, None]:
    lines_chunk: list[str] = []
    symbols_count = 0
    for line in text.split('\n'):
        line_symbols_count = len(line)
        if (symbols_count + line_symbols_count) >= CHUNK_SYMBOLS_COUNT:
            yield '\n'.join(lines_chunk)
            lines_chunk.clear()
            symbols_count = 0
        lines_chunk.append(line)
        symbols_count += line_symbols_count
    yield '\n'.join(lines_chunk)


def abbreviate_time_units(text: str) -> str:
    abbreviations = ('дн', 'ч', 'мин')
    new_word = ''
    for word in text.split():
        for abbreviation in abbreviations:
            if word.startswith(abbreviation):
                word = abbreviation
        new_word += ' ' + word
    return new_word


def intgaps(number: int | float) -> str:
    """Make big numbers more readable.

    Examples:
        >>> intgaps(43466456)
        '43 466 456'
        >>> intgaps(5435.5)
        '5 435.5'

    Args:
        number: Any number.

    Returns:
        Readable big digit.
    """
    return f'{number:_}'.replace('_', ' ')
