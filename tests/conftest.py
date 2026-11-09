import pytest
import os
if os.environ.get('SONGS_TEST_MOCK') == '1':
    import pymongo
    import mongomock
    pymongo.MongoClient = mongomock.MongoClient
    os.environ.setdefault('MONGODB_SERVICE', 'localhost')
from backend import app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def picture():
    picture = {
        "id": 200,
        "pic_url": "http://dummyimage.com/230x100.png/dddddd/000000",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "11/2/2030"
    }
    return dict(picture)
