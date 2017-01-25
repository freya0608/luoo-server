import json

import pytest
from sanic.utils import sanic_endpoint_test


@pytest.fixture(scope="module")
def app_for_test():
    from app import app
    return app


def test_app_root(app_for_test):
    request, response = sanic_endpoint_test(app_for_test, uri="/")
    assert response.text == json.dumps({'hello': 'world'}, separators=(',', ':'))


def test_get_(app_for_test):
    song_id = "1"
    request, response = sanic_endpoint_test(app_for_test, uri=("/songs/%s" % song_id))
    assert response.text == "Getting download url of song: {}".format(song_id)
