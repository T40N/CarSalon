import pytest
from app.models import Salon
from app.repositories import SalonRepository
from app import db


@pytest.fixture(scope='function')
def setup_salon(init_database):
    salon = None
    try:
        salon = Salon(name='Test Salon')
        db.session.add(salon)
        db.session.commit()

        yield salon
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        if salon:
            db.session.delete(salon)
            db.session.commit()


def test_create(init_database):
    # Initialisation
    salon = Salon(name='New Test Salon')

    # Progress
    created_salon = SalonRepository.create(salon)

    # Assertions
    assert created_salon.name == 'New Test Salon'
    assert Salon.query.count() == 1

    # Cleanup
    db.session.delete(created_salon)
    db.session.commit()
    assert Salon.query.count() == 0


def test_get_all(init_database, setup_salon):
    # Initialisation
    salon1 = setup_salon
    salon2 = Salon(name='Another Test Salon')
    db.session.add(salon2)
    db.session.commit()

    # Progress
    salons = SalonRepository.get_all()

    # Assertions
    assert len(salons) == 2
    assert salon1 in salons
    assert salon2 in salons

    # Cleanup
    db.session.delete(salon2)
    db.session.commit()
    assert Salon.query.count() == 1


def test_get_by_id(init_database, setup_salon):
    # Initialisation
    salon = setup_salon

    # Progress
    fetched_salon = SalonRepository.get_by_id(salon.id)

    # Assertions
    assert fetched_salon.id == salon.id
    assert fetched_salon.name == 'Test Salon'


def test_update(init_database, setup_salon):
    # Initialisation
    salon = setup_salon
    salon.name = 'Updated Test Salon'

    # Progress
    updated_salon = SalonRepository.update(salon.id, {'name': salon.name})

    # Assertions
    assert updated_salon.name == 'Updated Test Salon'
    assert Salon.query.get(salon.id).name == 'Updated Test Salon'


def test_delete(init_database, setup_salon):
    # Initialisation
    salon = setup_salon

    # Progress
    SalonRepository.delete(salon)

    # Assertions
    assert Salon.query.get(salon.id) is None
    assert Salon.query.count() == 0
