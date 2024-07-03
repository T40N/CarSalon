import pytest
from app.models import Address
from app.models import Salon
from app.repositories import AddressRepository
from app import db


@pytest.fixture(scope='function')
def setup_salons(init_database):
    salon1, salon2 = None, None
    try:
        salon1 = Salon(name='Test Salon 1')
        salon2 = Salon(name='Test Salon 2')
        db.session.add(salon1)
        db.session.add(salon2)
        db.session.commit()

        yield salon1, salon2
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        if salon1:
            db.session.delete(salon1)
        if salon2:
            db.session.delete(salon2)
        db.session.commit()


@pytest.fixture(scope='function')
def setup_address(init_database, setup_salons):
    salon1, _ = setup_salons
    address = None
    try:
        address = Address(street='Test Street', city='Test City', state='Test State', zip_code='12345', salon_id=salon1.id)
        db.session.add(address)
        db.session.commit()

        yield address
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        if address:
            db.session.delete(address)
            db.session.commit()


def test_create(init_database, setup_salons):
    salon1, _ = setup_salons
    # Initialisation
    address = Address(street='New Street', city='New City', state='New State', zip_code='67890', salon_id=salon1.id)

    # Progress
    created_address = AddressRepository.create(address)

    # Assertions
    assert created_address.street == 'New Street'
    assert created_address.city == 'New City'
    assert created_address.state == 'New State'
    assert created_address.zip_code == '67890'
    assert created_address.salon_id == salon1.id
    assert Address.query.count() == 1

    # Cleanup
    db.session.delete(created_address)
    db.session.commit()
    assert Address.query.count() == 0


def test_get_all(init_database, setup_address, setup_salons):
    _, salon2 = setup_salons
    # Initialisation
    address1 = setup_address
    address2 = Address(street='Another Street', city='Another City', state='Another State', zip_code='54321',
                       salon_id=salon2.id)
    db.session.add(address2)
    db.session.commit()

    # Progress
    addresses = AddressRepository.get_all()

    # Assertions
    assert len(addresses) == 2
    assert address1 in addresses
    assert address2 in addresses

    # Cleanup
    db.session.delete(address2)
    db.session.commit()
    assert Address.query.count() == 1


def test_get_by_id(init_database, setup_address):
    # Initialisation
    address = setup_address

    # Progress
    fetched_address = AddressRepository.get_by_id(address.id)

    # Assertions
    assert fetched_address.id == address.id
    assert fetched_address.street == 'Test Street'
    assert fetched_address.city == 'Test City'
    assert fetched_address.state == 'Test State'
    assert fetched_address.zip_code == '12345'


def test_update(init_database, setup_address):
    # Initialisation
    address = setup_address
    address.street = 'Updated Street'

    # Progress
    updated_address = AddressRepository.update(address.id, {'street': 'Updated Street'})

    # Assertions
    assert updated_address.street == 'Updated Street'
    assert Address.query.get(address.id).street == 'Updated Street'


def test_delete(init_database, setup_address):
    # Initialisation
    address = setup_address

    # Progress
    AddressRepository.delete(address)

    # Assertions
    assert Address.query.get(address.id) is None
    assert Address.query.count() == 0
