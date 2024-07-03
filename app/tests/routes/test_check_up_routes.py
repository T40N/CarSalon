import json
import pytest
from datetime import date
from app import db
from app.models import CheckUp
from app.models import Vehicle
from app.models import Salon


@pytest.fixture(scope='function')
def setup_salon_and_vehicles():
    salon = Salon(name='Test Salon')
    db.session.add(salon)
    db.session.commit()
    vehicle1 = Vehicle(name='Test Car 1', salon_id=salon.id)
    vehicle2 = Vehicle(name='Test Car 2', salon_id=salon.id)
    db.session.add(vehicle1)
    db.session.add(vehicle2)
    db.session.commit()
    yield salon, vehicle1, vehicle2
    db.session.delete(vehicle1)
    db.session.delete(vehicle2)
    db.session.delete(salon)
    db.session.commit()


def test_get_checkups_empty(test_client, init_database):
    # Progress
    response = test_client.get('/api/checkups/')

    # Assertions
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_checkups(test_client, init_database, setup_salon_and_vehicles):
    # Initialisation
    salon, vehicle1, vehicle2 = setup_salon_and_vehicles
    checkup1 = CheckUp(last_checkup_date=date.today(), notes='Checkup 1', vehicle_id=vehicle1.id)
    checkup2 = CheckUp(last_checkup_date=date.today(), notes='Checkup 2', vehicle_id=vehicle2.id)
    db.session.add(checkup1)
    db.session.add(checkup2)
    db.session.commit()

    # Progress
    response = test_client.get('/api/checkups/')

    # Assertions
    assert response.status_code == 200
    assert len(response.get_json()) == 2

    # Cleanup
    db.session.delete(checkup1)
    db.session.delete(checkup2)
    db.session.commit()


def test_get_checkup(test_client, init_database, setup_salon_and_vehicles):
    # Initialisation
    salon, vehicle1, _ = setup_salon_and_vehicles
    checkup = CheckUp(last_checkup_date=date.today(), notes='Test Checkup', vehicle_id=vehicle1.id)
    db.session.add(checkup)
    db.session.commit()

    # Progress
    response = test_client.get(f'/api/checkups/{checkup.id}')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()['notes'] == 'Test Checkup'

    # Cleanup
    db.session.delete(checkup)
    db.session.commit()


def test_get_checkup_not_found(test_client, init_database):
    # Progress
    response = test_client.get('/api/checkups/999')

    # Assertions
    assert response.status_code == 404


def test_create_checkup(test_client, init_database, setup_salon_and_vehicles):
    # Initialisation
    salon, vehicle1, _ = setup_salon_and_vehicles
    data = {
        'last_checkup_date': date.today().isoformat(),
        'notes': 'New Checkup',
        'vehicle_id': vehicle1.id
    }

    # Progress
    response = test_client.post('/api/checkups/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 201
    assert response.get_json()['notes'] == 'New Checkup'
    assert CheckUp.query.count() == 1

    # Cleanup
    created_checkup = CheckUp.query.first()
    db.session.delete(created_checkup)
    db.session.commit()
    assert CheckUp.query.count() == 0


def test_create_checkup_invalid_data(test_client, init_database):
    # Initialisation
    data = {}

    # Progress
    response = test_client.post('/api/checkups/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 400


def test_update_checkup(test_client, init_database, setup_salon_and_vehicles):
    # Initialisation
    salon, vehicle1, _ = setup_salon_and_vehicles
    checkup = CheckUp(last_checkup_date=date.today(), notes='Old Checkup', vehicle_id=vehicle1.id)
    db.session.add(checkup)
    db.session.commit()
    data = {'notes': 'Updated Checkup'}
    checkup_id = checkup.id

    # Debugging: check initial state
    assert CheckUp.query.get(checkup_id).notes == 'Old Checkup'

    # Progress
    response = test_client.put(f'/api/checkups/{checkup.id}', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()
    assert response.get_json()['notes'] == 'Updated Checkup'

    # Cleanup
    db.session.delete(checkup)
    db.session.commit()


def test_update_checkup_not_found(test_client, init_database):
    # Initialisation
    data = {'notes': 'Updated Checkup'}

    # Progress
    response = test_client.put('/api/checkups/999', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 404


def test_delete_checkup(test_client, init_database, setup_salon_and_vehicles):
    # Initialisation
    salon, vehicle1, _ = setup_salon_and_vehicles
    checkup = CheckUp(last_checkup_date=date.today(), notes='Checkup to Delete', vehicle_id=vehicle1.id)
    db.session.add(checkup)
    db.session.commit()

    # Progress
    response = test_client.delete(f'/api/checkups/{checkup.id}')

    # Assertions
    assert response.status_code == 204


def test_delete_checkup_not_found(test_client, init_database):
    # Progress
    response = test_client.delete('/api/checkups/999')

    # Assertions
    assert response.status_code == 404