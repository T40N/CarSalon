import json
import pytest
from app import db
from app.models import Address
from app.models import Salon


@pytest.fixture(scope='function')
def setup_salons():
    salon1 = Salon(name='Test Salon 1')
    salon2 = Salon(name='Test Salon 2')
    db.session.add(salon1)
    db.session.add(salon2)
    db.session.commit()
    yield salon1, salon2
    db.session.delete(salon1)
    db.session.delete(salon2)
    db.session.commit()


def test_get_addresses_empty(test_client, init_database):
    # Progress
    response = test_client.get('/api/address/')

    # Assertions
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_addresses(test_client, init_database, setup_salons):
    # Initialisation
    salon1, salon2 = setup_salons
    address1 = Address(street='Street 1', city='City 1', state='State 1', zip_code='11111', salon_id=salon1.id)
    address2 = Address(street='Street 2', city='City 2', state='State 2', zip_code='22222', salon_id=salon2.id)
    db.session.add(address1)
    db.session.add(address2)
    db.session.commit()

    # Progress
    response = test_client.get('/api/address/')

    # Assertions
    assert response.status_code == 200
    assert len(response.get_json()) == 2

    # Cleanup
    db.session.delete(address1)
    db.session.delete(address2)
    db.session.commit()


def test_get_address(test_client, init_database, setup_salons):
    # Initialisation
    salon1, _ = setup_salons
    address = Address(street='Test Street', city='Test City', state='Test State', zip_code='12345', salon_id=salon1.id)
    db.session.add(address)
    db.session.commit()

    # Progress
    response = test_client.get(f'/api/address/{address.id}')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()['street'] == 'Test Street'

    # Cleanup
    db.session.delete(address)
    db.session.commit()


def test_get_address(test_client, init_database, setup_salons):
    # Initialisation
    salon1, _ = setup_salons
    address = Address(street='Test Street', city='Test City', state='Test State', zip_code='12345', salon_id=salon1.id)
    db.session.add(address)
    db.session.commit()

    # Progress
    response = test_client.get(f'/api/address/{address.id}')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()['street'] == 'Test Street'

    # Cleanup
    db.session.delete(address)
    db.session.commit()


def test_get_address_not_found(test_client, init_database):
    # Progress
    response = test_client.get('/api/address/999')

    # Assertions
    assert response.status_code == 404


def test_create_address(test_client, init_database, setup_salons):
    # Initialisation
    salon1, _ = setup_salons
    data = {
        'street': 'New Street',
        'city': 'New City',
        'state': 'New State',
        'zip_code': '54321',
        'salon_id': salon1.id
    }

    # Progress
    response = test_client.post('/api/address/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 201
    assert response.get_json()['street'] == 'New Street'
    assert Address.query.count() == 1

    # Cleanup
    created_address = Address.query.first()
    db.session.delete(created_address)
    db.session.commit()
    assert Address.query.count() == 0


def test_create_address_invalid_data(test_client, init_database):
    # Initialisation
    data = {}

    # Progress
    response = test_client.post('/api/address/', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 400


def test_update_address(test_client, init_database, setup_salons):
    # Initialisation
    salon1, _ = setup_salons
    address = Address(street='Old Street', city='Old City', state='Old State', zip_code='12345', salon_id=salon1.id)
    db.session.add(address)
    db.session.commit()
    data = {'street': 'Updated Street'}
    address_id = address.id

    # Debugging: check initial state
    assert Address.query.get(address_id).street == 'Old Street'

    # Progress
    response = test_client.put(f'/api/address/{address.id}', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 200
    assert response.get_json()
    assert response.get_json()['street'] == 'Updated Street'

    # Cleanup
    db.session.delete(address)
    db.session.commit()


def test_update_address_not_found(test_client, init_database):
    # Initialisation
    data = {'street': 'Updated Street'}

    # Progress
    response = test_client.put('/api/address/999', data=json.dumps(data), content_type='application/json')

    # Assertions
    assert response.status_code == 404


def test_delete_address(test_client, init_database, setup_salons):
    # Initialisation
    salon1, _ = setup_salons
    address = Address(street='Street to Delete', city='City to Delete', state='State to Delete', zip_code='12345',
                      salon_id=salon1.id)
    db.session.add(address)
    db.session.commit()

    # Progress
    response = test_client.delete(f'/api/address/{address.id}')

    # Assertions
    assert response.status_code == 204


def test_delete_address_not_found(test_client, init_database):
    # Progress
    response = test_client.delete('/api/address/999')

    # Assertions
    assert response.status_code == 404
