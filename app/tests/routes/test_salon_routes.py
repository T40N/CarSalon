import json
import pytest
from app import create_app, db
from app.models.salon import Salon


# @pytest.fixture(scope='module')
# def test_client():
#     flask_app = create_app()
#     with flask_app.test_client() as testing_client:
#         with flask_app.app_context():
#             yield testing_client
#
#
# @pytest.fixture(scope='function')
# def init_database():
#     db.create_all()
#     yield db
#     db.session.remove()
#     db.drop_all()


def test_get_salons_empty(test_client, init_database):
    # Progress
    response = test_client.get('/api/salons/')

    # Assertions
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_salons(test_client, init_database):
    # Initialisation
    salon1 = Salon(name='Salon 1')
    salon2 = Salon(name='Salon 2')
    db.session.add(salon1)
    db.session.add(salon2)
    db.session.commit()

    # Progress
    response = test_client.get('/api/salons/')

    # Assertions
    assert response.status_code == 200
    assert len(response.get_json()) == 2

    # Cleanup
    db.session.delete(salon1)
    db.session.delete(salon2)
    db.session.commit()


def test_get_salon(test_client, init_database):
    # Initialisation
    salon = Salon(name='Test Salon')
    db.session.add(salon)
    db.session.commit()

    # Progress
    response = test_client.get(f'/api/salons/{salon.id}')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Test Salon'

    # Cleanup
    db.session.delete(salon)
    db.session.commit()


def test_get_salon_not_found(test_client, init_database):
    # Progress
    response = test_client.get('/api/salons/999')

    # Assertions
    assert response.status_code == 404


def test_create_salon(test_client, init_database):
    # Initialisation
    data = {'name': 'New Salon'}

    # Progress
    response = test_client.post('/api/salons/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 201
    assert response.get_json()['name'] == 'New Salon'
    assert Salon.query.count() == 1

    # Cleanup
    created_salon = Salon.query.first()
    db.session.delete(created_salon)
    db.session.commit()
    assert Salon.query.count() == 0


def test_create_salon_invalid_data(test_client, init_database):
    # Initialisation
    data = {}

    # Progress
    response = test_client.post('/api/salons/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 400


def test_update_salon(test_client, init_database):
    # Initialisation
    salon = Salon(name='Old Salon')
    db.session.add(salon)
    db.session.commit()
    data = {'name': 'Updated Salon'}
    salon_id = salon.id

    # Debugging: check initial state
    assert Salon.query.get(salon_id).name == 'Old Salon'

    # Progress
    response = test_client.put(f'/api/salons/{salon.id}', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()
    assert response.get_json()['name'] == 'Updated Salon'

    # Cleanup
    db.session.delete(salon )
    db.session.commit()


def test_update_salon_not_found(test_client, init_database):
    # Initialisation
    data = {'name': 'Updated Salon'}

    # Progress
    response = test_client.put('/api/salons/999', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 404


def test_delete_salon(test_client, init_database):
    # Initialisation
    salon = Salon(name='Salon to Delete')
    db.session.add(salon)
    db.session.commit()

    # Progress
    response = test_client.delete(f'/api/salons/{salon.id}')

    # Assertions
    assert response.status_code == 204


def test_delete_salon_not_found(test_client, init_database):
    # Progress
    response = test_client.delete('/api/salons/999')

    # Assertions
    assert response.status_code == 404
