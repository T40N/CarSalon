import pytest
from app.controllers import AddressController
from app.models import Address
from app.models import Salon
from app import db


@pytest.fixture(scope='function')
def setup_salons(init_database):
    salon1 = Salon(name='Test Salon 1')
    salon2 = Salon(name='Test Salon 2')
    db.session.add(salon1)
    db.session.add(salon2)
    db.session.commit()

    yield salon1, salon2

    db.session.delete(salon1)
    db.session.delete(salon2)
    db.session.commit()


def test_create_address(init_database, setup_salons):
    salon1, salon2 = setup_salons
    # Initialisation
    data = {
        'street': 'Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'zip_code': '12345',
        'salon_id': salon1.id
    }

    # Progress
    address = AddressController.create_address(data)

    # Assertions
    assert address.street == 'Test Street'
    assert address.city == 'Test City'
    assert address.state == 'Test State'
    assert address.zip_code == '12345'
    assert address.salon_id == salon1.id
    assert Address.query.count() == 1

    # Cleanup
    db.session.delete(address)
    db.session.commit()
    assert Address.query.count() == 0


def test_get_all_addresses(init_database, setup_salons):
    salon1, salon2 = setup_salons
    # Initialisation
    address1 = Address(street='Street 1', city='City 1', state='State 1', zip_code='11111', salon_id=salon1.id)
    address2 = Address(street='Street 2', city='City 2', state='State 2', zip_code='22222', salon_id=salon2.id)
    db.session.add(address1)
    db.session.add(address2)
    db.session.commit()

    # Progress
    addresses = AddressController.get_all_addresses()

    # Assertions
    assert len(addresses) == 2
    assert address1 in addresses
    assert address2 in addresses

    # Cleanup
    db.session.delete(address1)
    db.session.delete(address2)
    db.session.commit()
    assert Address.query.count() == 0


def test_get_address_by_id(init_database, setup_salons):
    salon1, salon2 = setup_salons
    # Initialisation
    address = Address(street='Street 1', city='City 1', state='State 1', zip_code='11111', salon_id=salon1.id)
    db.session.add(address)
    db.session.commit()
    address_id = address.id

    # Progress
    fetched_address = AddressController.get_address_by_id(address_id)

    # Assertions
    assert fetched_address.id == address_id
    assert fetched_address.street == 'Street 1'
    assert fetched_address.city == 'City 1'
    assert fetched_address.state == 'State 1'
    assert fetched_address.zip_code == '11111'

    # Cleanup
    db.session.delete(address)
    db.session.commit()
    assert Address.query.count() == 0


def test_update_address(init_database, setup_salons):
    salon1, salon2 = setup_salons
    # Initialisation
    address = Address(street='Street 1', city='City 1', state='State 1', zip_code='11111', salon_id=salon1.id)
    db.session.add(address)
    db.session.commit()
    address_id = address.id

    update_data = {'street': 'Updated Street', 'city': 'Updated City'}

    # Progress
    updated_address = AddressController.update_address(address_id, update_data)

    # Assertions
    assert updated_address.street == 'Updated Street'
    assert updated_address.city == 'Updated City'
    assert Address.query.get(address_id).street == 'Updated Street'
    assert Address.query.get(address_id).city == 'Updated City'

    # Cleanup
    db.session.delete(updated_address)
    db.session.commit()
    assert Address.query.count() == 0


def test_delete_address(init_database, setup_salons):
    salon1, salon2 = setup_salons
    # Initialisation
    address = Address(street='Street 1', city='City 1', state='State 1', zip_code='11111', salon_id=salon1.id)
    db.session.add(address)
    db.session.commit()
    address_id = address.id

    # Progress
    success = AddressController.delete_address(address_id)

    # Assertions
    assert success
    assert Address.query.get(address_id) is None

    # Cleanup
    assert Address.query.count() == 0
