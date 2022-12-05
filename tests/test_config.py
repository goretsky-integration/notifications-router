import os
import tempfile

from config import load_config


def test_load_config():
    temp_config_file_path = './config.tmp.ini'

    with open(temp_config_file_path, 'w') as file:
        file.write('''[app]
telegram_bot_token = 15135645243:gakFjFbDwfFHsf-FhdfFRfkPdFbgfDF-L
database_api_url = http://localhost:8000/database
rabbitmq_url = amqp://localhost:5672
debug = true''')

    config = load_config(temp_config_file_path)
    if os.path.exists(temp_config_file_path):
        os.remove(temp_config_file_path)

    assert config.debug == True
    assert config.rabbitmq_url == 'amqp://localhost:5672'
    assert config.telegram_bot_token == '15135645243:gakFjFbDwfFHsf-FhdfFRfkPdFbgfDF-L'
    assert config.database_api_url == 'http://localhost:8000/database'
