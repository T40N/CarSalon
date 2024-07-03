import pytest
from datetime import date
from app.models import CheckUp
from app.models import Vehicle
from app.models import Salon
from app.repositories import CheckUpRepository
from app import db


@pytest.fixture(scope='function')
def setup_salon_and_vehicles(init_database):
    salon, vehicle1, vehicle2 = None, None, None
    try:
        salon = Salon(name='Test Salon')
        db.session.add(salon)
        db.session.commit()  # Save the salon first

        vehicle1 = Vehicle(name='Test Car 1', salon_id=salon.id)
        vehicle2 = Vehicle(name='Test Car 2', salon_id=salon.id)
        db.session.add(vehicle1)
        db.session.add(vehicle2)
        db.session.commit()

        yield salon, vehicle1, vehicle2
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        if vehicle1:
            db.session.delete(vehicle1)
        if vehicle2:
            db.session.delete(vehicle2)
        if salon:
            db.session.delete(salon)
        db.session.commit()


@pytest.fixture(scope='function')
def setup_checkup(init_database, setup_salon_and_vehicles):
    try:
        _, vehicle1, _ = setup_salon_and_vehicles
        checkup = CheckUp(last_checkup_date=date.today(), notes='Test Checkup', vehicle_id=vehicle1.id)
        db.session.add(checkup)
        db.session.commit()

        yield checkup
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        if checkup:
            db.session.delete(checkup)
        db.session.commit()


def test_create(init_database, setup_salon_and_vehicles):
    _, vehicle1, _ = setup_salon_and_vehicles
    # Initialisation
    checkup = CheckUp(last_checkup_date=date.today(), notes='New Checkup', vehicle_id=vehicle1.id)

    # Progress
    created_checkup = CheckUpRepository.create(checkup)

    # Assertions
    assert created_checkup.last_checkup_date == date.today()
    assert created_checkup.notes == 'New Checkup'
    assert created_checkup.vehicle_id == vehicle1.id
    assert CheckUp.query.count() == 1

    # Cleanup
    db.session.delete(created_checkup)
    db.session.commit()
    assert CheckUp.query.count() == 0


def test_get_all(init_database, setup_salon_and_vehicles):
    _, vehicle1, vehicle2 = setup_salon_and_vehicles
    # Initialisation
    checkup1 = CheckUp(last_checkup_date=date.today(), notes='Checkup 1', vehicle_id=vehicle1.id)
    checkup2 = CheckUp(last_checkup_date=date.today(), notes='Checkup 2', vehicle_id=vehicle2.id)
    db.session.add(checkup1)
    db.session.add(checkup2)
    db.session.commit()

    # Progress
    checkups = CheckUpRepository.get_all()

    # Assertions
    assert len(checkups) == 2
    assert checkup1 in checkups
    assert checkup2 in checkups

    # Cleanup
    db.session.delete(checkup1)
    db.session.delete(checkup2)
    db.session.commit()
    assert CheckUp.query.count() == 0


def test_get_by_id(init_database, setup_checkup):
    # Initialisation
    checkup = setup_checkup

    # Progress
    fetched_checkup = CheckUpRepository.get_by_id(checkup.id)

    # Assertions
    assert fetched_checkup.id == checkup.id
    assert fetched_checkup.last_checkup_date == checkup.last_checkup_date
    assert fetched_checkup.notes == checkup.notes
    assert fetched_checkup.vehicle_id == checkup.vehicle_id


def test_update(init_database, setup_checkup):
    # Initialisation
    checkup = setup_checkup

    # Progress
    updated_checkup = CheckUpRepository.update(checkup.id, {'notes': 'Updated Checkup'})

    # Assertions
    assert updated_checkup.notes == 'Updated Checkup'
    assert CheckUp.query.get(checkup.id).notes == 'Updated Checkup'


def test_delete(init_database, setup_checkup):
    # Initialisation
    checkup = setup_checkup

    # Progress
    CheckUpRepository.delete(checkup)

    # Assertions
    assert CheckUp.query.get(checkup.id) is None
    assert CheckUp.query.count() == 0
