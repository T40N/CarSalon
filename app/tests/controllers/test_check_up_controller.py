import pytest
from datetime import date
from app.controllers import CheckUpController
from app.models import CheckUp
from app.models import Vehicle
from app.models import Salon
from app import db


@pytest.fixture(scope='function')
def setup_vehicle(init_database):
    salon = Salon(name='Test Salon')
    db.session.add(salon)
    db.session.commit()

    vehicle1 = Vehicle(name='Test Car 1', salon_id=salon.id)
    vehicle2 = Vehicle(name='Test Car 2', salon_id=salon.id)
    db.session.add(vehicle1)
    db.session.add(vehicle2)
    db.session.commit()

    yield vehicle1, vehicle2

    db.session.delete(vehicle1)
    db.session.delete(vehicle2)
    db.session.delete(salon)
    db.session.commit()


def test_create_checkup(init_database, setup_vehicle):
    vehicle1, vehicle2 = setup_vehicle
    # Initialisation
    data = {'last_checkup_date': date.today(), 'notes': 'Przegląd testowy', 'vehicle_id': vehicle1.id}

    # Progress
    checkup = CheckUpController.create_checkup(data)

    # Assertions
    assert checkup.last_checkup_date == date.today()
    assert checkup.notes == 'Przegląd testowy'
    assert checkup.vehicle_id == vehicle1.id
    assert CheckUp.query.count() == 1

    # Cleanup
    db.session.delete(checkup)
    db.session.commit()
    assert CheckUp.query.count() == 0


def test_get_all_checkups(init_database, setup_vehicle):
    vehicle1, vehicle2 = setup_vehicle
    # Initialisation
    checkup1 = CheckUp(last_checkup_date=date.today(), notes='Przegląd testowy 1', vehicle_id=vehicle1.id)
    checkup2 = CheckUp(last_checkup_date=date.today(), notes='Przegląd testowy 2', vehicle_id=vehicle2.id)
    db.session.add(checkup1)
    db.session.add(checkup2)
    db.session.commit()

    # Progress
    checkups = CheckUpController.get_all_checkups()

    # Assertions
    assert len(checkups) == 2
    assert checkup1 in checkups
    assert checkup2 in checkups

    # Cleanup
    db.session.delete(checkup1)
    db.session.delete(checkup2)
    db.session.commit()
    assert CheckUp.query.count() == 0


def test_get_checkup_by_id(init_database, setup_vehicle):
    vehicle1, vehicle2 = setup_vehicle
    # Initialisation
    checkup = CheckUp(last_checkup_date=date.today(), notes='Przegląd testowy', vehicle_id=vehicle1.id)
    db.session.add(checkup)
    db.session.commit()
    checkup_id = checkup.id

    # Progress
    fetched_checkup = CheckUpController.get_checkup_by_id(checkup_id)

    # Assertions
    assert fetched_checkup.id == checkup_id
    assert fetched_checkup.notes == 'Przegląd testowy'

    # Cleanup
    db.session.delete(checkup)
    db.session.commit()
    assert CheckUp.query.count() == 0


def test_update_checkup(init_database, setup_vehicle):
    vehicle1, vehicle2 = setup_vehicle
    # Initialisation
    checkup = CheckUp(last_checkup_date=date.today(), notes='Przegląd testowy', vehicle_id=vehicle1.id)
    db.session.add(checkup)
    db.session.commit()
    checkup_id = checkup.id

    update_data = {'notes': 'Zaktualizowane notatki'}

    # Progress
    updated_checkup = CheckUpController.update_checkup(checkup_id, update_data)

    # Assertions
    assert updated_checkup.notes == 'Zaktualizowane notatki'
    assert CheckUp.query.get(checkup_id).notes == 'Zaktualizowane notatki'

    # Cleanup
    db.session.delete(updated_checkup)
    db.session.commit()
    assert CheckUp.query.count() == 0


def test_delete_checkup(init_database, setup_vehicle):
    vehicle1, vehicle2 = setup_vehicle
    # Initialisation
    checkup = CheckUp(last_checkup_date=date.today(), notes='Przegląd testowy', vehicle_id=vehicle1.id)
    db.session.add(checkup)
    db.session.commit()
    checkup_id = checkup.id

    # Progress
    success = CheckUpController.delete_checkup(checkup_id)

    # Assertions
    assert success
    assert CheckUp.query.get(checkup_id) is None

    # Cleanup
    assert CheckUp.query.count() == 0
