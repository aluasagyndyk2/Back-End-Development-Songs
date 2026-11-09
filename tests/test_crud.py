"""Unit checks with a MongoDB test double; live curl evidence is collected separately."""
import os
import importlib
from unittest.mock import patch
import mongomock

os.environ.setdefault('MONGODB_SERVICE', 'localhost')
with patch('pymongo.MongoClient', mongomock.MongoClient):
    backend = importlib.import_module('backend')


def test_song_crud():
    client = backend.app.test_client()
    assert client.get('/health').json == {'status': 'OK'}
    count = client.get('/count').json['length']
    song = {'id': 9001, 'title': 'Capstone test', 'lyrics': 'Original test lyrics'}
    assert client.post('/song', json=song).status_code == 201
    assert client.post('/song', json=song).status_code == 302
    assert client.get('/count').json['length'] == count + 1
    assert client.get('/song/9001').json['title'] == song['title']
    song['title'] = 'Updated title'
    assert client.put('/song/9001', json=song).status_code == 200
    assert client.get('/song/9001').json['title'] == song['title']
    assert client.delete('/song/9001').status_code == 204
    assert client.get('/song/9001').status_code == 404
    assert client.get('/count').json['length'] == count


def test_missing_song_and_invalid_body():
    client = backend.app.test_client()
    assert client.get('/song/987654').status_code == 404
    assert client.put('/song/987654', json={'id': 987654}).status_code == 404
    assert client.delete('/song/987654').status_code == 404
    assert client.post('/song', json={}).status_code == 400
