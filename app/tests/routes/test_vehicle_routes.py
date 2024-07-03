import json
import pytest
from app import db
from app.models import Vehicle
from app.models import Salon


@pytest.fixture(scope='function')
def setup_salon():
    salon = Salon(name='Test Salon')
    db.session.add(salon)
    db.session.commit()
    yield salon
    db.session.delete(salon)
    db.session.commit()


def test_get_vehicles_empty(test_client, init_database):
    # Progress
    response = test_client.get('/api/vehicles/')

    # Assertions
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_vehicles(test_client, init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    vehicle1 = Vehicle(name='Car 1', salon_id=salon.id)
    vehicle2 = Vehicle(name='Car 2', salon_id=salon.id)
    db.session.add(vehicle1)
    db.session.add(vehicle2)
    db.session.commit()

    # Progress
    response = test_client.get('/api/vehicles/')

    # Assertions
    assert response.status_code == 200
    assert len(response.get_json()) == 2

    # Cleanup
    db.session.delete(vehicle1)
    db.session.delete(vehicle2)
    db.session.commit()


def test_get_vehicle(test_client, init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    vehicle = Vehicle(name='Test Car', salon_id=salon.id)
    db.session.add(vehicle)
    db.session.commit()

    # Progress
    response = test_client.get(f'/api/vehicles/{vehicle.id}')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Test Car'

    # Cleanup
    db.session.delete(vehicle)
    db.session.commit()


def test_get_vehicle_not_found(test_client, init_database):
    # Progress
    response = test_client.get('/api/vehicles/999')

    # Assertions
    assert response.status_code == 404


def test_create_vehicle(test_client, init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    data = {'name': 'New Car', 'salon_id': salon.id}

    # Progress
    response = test_client.post('/api/vehicles/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 201
    assert response.get_json()['name'] == 'New Car'
    assert Vehicle.query.count() == 1

    # Cleanup
    created_vehicle = Vehicle.query.first()
    db.session.delete(created_vehicle)
    db.session.commit()
    assert Vehicle.query.count() == 0


def test_create_vehicle_invalid_data(test_client, init_database):
    # Initialisation
    data = {}

    # Progress
    response = test_client.post('/api/vehicles/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 400


def test_update_vehicle(test_client, init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    vehicle = Vehicle(name='Old Car', salon_id=salon.id)
    db.session.add(vehicle)
    db.session.commit()
    data = {'name': 'Updated Car'}
    vehicle_id = vehicle.id

    # Debugging: check initial state
    assert Vehicle.query.get(vehicle_id).name == 'Old Car'

    # Progress
    response = test_client.put(f'/api/vehicles/{vehicle.id}', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()
    assert response.get_json()['name'] == 'Updated Car'

    # Cleanup
    db.session.delete(vehicle)
    db.session.commit()


def test_update_vehicle_not_found(test_client, init_database):
    # Initialisation
    data = {'name': 'Updated Car'}

    # Progress
    response = test_client.put('/api/vehicles/999', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 404


def test_delete_vehicle(test_client, init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    vehicle = Vehicle(name='Car to Delete', salon_id=salon.id)
    db.session.add(vehicle)
    db.session.commit()

    # Progress
    response = test_client.delete(f'/api/vehicles/{vehicle.id}')

    # Assertions
    assert response.status_code == 204


def test_delete_vehicle_not_found(test_client, init_database):
    # Progress
    response = test_client.delete('/api/vehicles/999')

    # Assertions
    assert response.status_code == 404


def test_pay_monthly_fee(test_client, init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    vehicle = Vehicle(name='Test Car', salon_id=salon.id)
    db.session.add(vehicle)
    db.session.commit()

    data = {'amount': 100.0}

    # Progress
    response = test_client.post(f'/api/vehicles/{vehicle.id}/pay', data=json.dumps(data),
                                content_type='application/json')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()
    assert response.get_json()['last_payment_date'] is not None

    # Cleanup
    db.session.delete(vehicle)
    db.session.commit()


def test_pay_monthly_fee_invalid_data(test_client, init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    vehicle = Vehicle(name='Test Car', salon_id=salon.id)
    db.session.add(vehicle)
    db.session.commit()

    data = {}

    # Progress
    response = test_client.post(f'/api/vehicles/{vehicle.id}/pay', data=json.dumps(data),
                                content_type='application/json')

    # Assertions
    assert response.status_code == 400

    # Cleanup
    db.session.delete(vehicle)
    db.session.commit()
