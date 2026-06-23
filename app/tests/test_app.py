import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c

def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'healthy'

def test_ready(client):
    assert client.get('/ready').status_code == 200

def test_index(client):
    assert client.get('/').get_json()['app'] == 'FlaskOps'

def test_orders(client):
    r = client.post('/orders', json={'item': 'laptop'})
    assert r.status_code in [201, 500]

def test_metrics(client):
    r = client.get('/metrics')
    assert r.status_code == 200
    assert b'flask' in r.data or b'# HELP' in r.data
