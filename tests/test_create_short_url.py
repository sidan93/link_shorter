import pytest
from http import client
import re

from fastapi.testclient import TestClient

from application.settings import SERVER_HOST, SERVER_PORT
from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "body,code",
    [
        ({}, 400),
        ({'visits': 1}, 400),
        ({'long_url': '34'}, 400),
        ({'long_url': 'google. com'}, 400),
        ({'long_url': 'google'}, 400),
    ]
)
def test_create_short_url_errors(body, code):
    responce = client.post('/urls/', json=body)
    assert responce.status_code == code, responce.json()

@pytest.mark.parametrize(
    "body",
    [
        ({'long_url': 'google.com'}),
        ({'long_url': 'http://google.com'}),
        ({'long_url': 'http://www.google.com'}),
    ]
)
def test_create_short_url(body):
    responce = client.post('/urls/', json=body)
    assert responce.status_code == 200, responce.json()
    pattern = re.compile(f'http:\/\/{SERVER_HOST}:{SERVER_PORT}\/urls\/.+')
    assert pattern.match(responce.json()) is not None
