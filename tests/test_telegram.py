import httpx

import telegram


class MockResponse:

    def json(*args, **kwargs):
        return {'ok': True}


def mock_post(*args, **kwargs) -> MockResponse:
    return MockResponse()


def test_telegram_send_message(monkeypatch):
    monkeypatch.setattr(httpx, 'post', mock_post)
    telegram_sender = telegram.TelegramSender('gdfijgijijigjsiefjsf')
    is_ok = telegram_sender.send_message(1234, 'hello')
    assert is_ok == True
