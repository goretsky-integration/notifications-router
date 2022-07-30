import pathlib

import pytest

import config
from text_utils import get_text_by_chunks, CHUNK_SYMBOLS_COUNT


@pytest.fixture
def big_text() -> str:
    file_path = pathlib.Path.joinpath(config.ROOT_PATH, 'tests', '40555_words_text.txt')
    with open(file_path, encoding='utf-8') as file:
        return file.read()


def test_text_chunk_size(big_text):
    for chunk in get_text_by_chunks(big_text):
        assert len(chunk) < CHUNK_SYMBOLS_COUNT


def test_text_chunks_count(big_text):
    words_count = len(big_text)
    chunks_count = words_count // CHUNK_SYMBOLS_COUNT
    if words_count % CHUNK_SYMBOLS_COUNT > 0:
        chunks_count += 1
    assert chunks_count == len(tuple(get_text_by_chunks(big_text)))
