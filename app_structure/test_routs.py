import pytest
import json

from flask import Flask, jsonify
from app_structure import create_app

@pytest.fixture
def client():
    app = create_app()
    app.app_context().push()

    return app.test_client()


def test_add_message(client):
  url = '/AddMessage'

  req = {
		"application_id" : 1,
		"session_id" : "aaa",
		"message_id" : "123",
		"participants" : [ "Mosheh", "Gad" ],
		"content" : "Hello to you"
  }
  
  res = client.post(url, data=json.dumps(req), content_type='application/json')
  assert res.status_code == 201

  req = {
		"application_id" : 1,
		"session_id" : "bbb",
		"message_id" : "124",
		"participants" : [ "Dan", "Gad" ],
		"content" : "Hi, how are you"
  }

  res = client.post(url, data=json.dumps(req), content_type='application/json')
  assert res.status_code == 201

  req = {
		"application_id" : 2,
		"session_id" : "aaa",
		"message_id" : "125",
		"participants" : [ "Ron", "Gad", "Avi" ],
		"content" : "Are you there?"
  }

  res = client.post(url, data=json.dumps(req), content_type='application/json')
  assert res.status_code == 201

  req = {
		"application_id" : 1,
		"session_id" : "aaa",
		"message_id" : "123",
		"participants" : [ "Ziv", "Gad", "Chaim" ],
		"content" : "Good morning"
    }

  res = client.post(url, data=json.dumps(req), content_type='application/json')
  assert res.status_code == 400

  req = {
		"name_id" : 1,
		"session_id" : "aaa",
		"message_id" : "231",
		"participants" : [ "Mosheh", "Gad" ],
		"content" : "Hello to you"
  }

  res = client.post(url, data=json.dumps(req), content_type='application/json')
  assert res.status_code == 400


def test_get_message(client):
  url = '/GetMessage'

  res = client.get(url + '?messageId=124',content_type='application/json')
  data = res.get_json()
  assert res.status_code == 200
  assert data.get('message_id') == '124'

  res = client.get(url + '?applicationId=1')
  data = res.get_json()
  for message in data.get('messages'):
    assert message.get('application_id') == 1
  assert res.status_code == 200

  res = client.get(url + '?sessionId=aaa')
  data = res.get_json()
  for message in data.get('messages'):
    assert message.get('session_id') == 'aaa'
  assert res.status_code == 200

  res = client.get(url + '?sessionId=hhh')
  assert res.status_code == 400

  res = client.get(url + '?hhhhh=jjj')
  assert res.status_code == 400


def test_delete_message():
  app = create_app()
  client = app.test_client()
  url = '/DeleteMessage'

  res = client.delete(url + '?hhhhh=jjj')
  assert res.status_code == 400

  res = client.delete(url + '?messageId=123')
  assert res.status_code == 200

  res = client.delete(url + '?sessionId=bbb')
  assert res.status_code == 200

  res = client.delete(url + '?sessionId=bbb')
  assert res.status_code == 400

  res = client.delete(url + '?applicationId=2')
  assert res.status_code == 200












  











