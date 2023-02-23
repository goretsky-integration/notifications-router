import httpx

import models
from db_api import DatabaseAPI


class MockResponse:

    def json(self):
        return [models.ReportRoute(chat_id=1234, unit_ids=(123, 234, 345))]


def mock_get(*args, **kwargs) -> MockResponse:
    return MockResponse()


def test_database_api_get_chats_to_retranslate(monkeypatch):
    monkeypatch.setattr(httpx, 'get', mock_get)
    database_api = DatabaseAPI('gdfjgosjifjsdiofj')
    reports = database_api.get_chats_to_retranslate('STATISTICS')
    assert reports == [models.ReportRoute(chat_id=1234, unit_ids=(123, 234, 345))]
