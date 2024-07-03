import json
import pytest
from app import db
from app.models import User


def test_get_users_empty(test_client, init_database):
    # Progress
    response = test_client.get('/api/users/')

    # Assertions
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_users(test_client, init_database):
    # Initialisation
    user1 = User(name='User 1')
    user2 = User(name='User 2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Progress
    response = test_client.get('/api/users/')

    # Assertions
    assert response.status_code == 200
    assert len(response.get_json()) == 2

    # Cleanup
    db.session.delete(user1)
    db.session.delete(user2)
    db.session.commit()


def test_get_user(test_client, init_database):
    # Initialisation
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()

    # Progress
    response = test_client.get(f'/api/users/{user.id}')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Test User'

    # Cleanup
    db.session.delete(user)
    db.session.commit()


def test_get_user_not_found(test_client, init_database):
    # Progress
    response = test_client.get('/api/users/999')

    # Assertions
    assert response.status_code == 404


def test_create_user(test_client, init_database):
    # Initialisation
    data = {'name': 'New User'}

    # Progress
    response = test_client.post('/api/users/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 201
    assert response.get_json()['name'] == 'New User'
    assert User.query.count() == 1

    # Cleanup
    created_user = User.query.first()
    db.session.delete(created_user)
    db.session.commit()
    assert User.query.count() == 0


def test_create_user_invalid_data(test_client, init_database):
    # Initialisation
    data = {}

    # Progress
    response = test_client.post('/api/users/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 400


def test_update_user(test_client, init_database):
    # Initialisation
    user = User(name='Old User')
    db.session.add(user)
    db.session.commit()
    data = {'name': 'Updated User'}
    user_id = user.id

    # Debugging: check initial state
    assert User.query.get(user_id).name == 'Old User'

    # Progress
    response = test_client.put(f'/api/users/{user.id}', data=json.dumps(data), content_type='application/json')


    # Assertions
    assert response.status_code == 200
    assert response.get_json()
    assert response.get_json()['name'] == 'Updated User'

    # Cleanup
    db.session.delete(user)
    db.session.commit()


def test_update_user_not_found(test_client, init_database):
    # Initialisation
    data = {'name': 'Updated User'}

    # Progress
    response = test_client.put('/api/users/999', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 404


def test_delete_user(test_client, init_database):
    # Initialisation
    user = User(name='User to Delete')
    db.session.add(user)
    db.session.commit()

    # Progress
    response = test_client.delete(f'/api/users/{user.id}')

    # Assertions
    assert response.status_code == 204


def test_delete_user_not_found(test_client, init_database):
    # Progress
    response = test_client.delete('/api/users/999')

    # Assertions
    assert response.status_code == 404