import pytest
from app.models import Vehicle
from app.models import Salon
from app.repositories import VehicleRepository
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


def test_create(init_database, setup_salon_and_vehicles):
    salon, _, _ = setup_salon_and_vehicles
    # Initialisation
    vehicle = Vehicle(name='New Car', salon_id=salon.id)

    # Progress
    created_vehicle = VehicleRepository.create(vehicle)

    # Assertions
    assert created_vehicle.name == 'New Car'
    assert created_vehicle.salon_id == salon.id
    assert Vehicle.query.count() == 3  # Including the two created in fixture

    # Cleanup
    db.session.delete(created_vehicle)
    db.session.commit()
    assert Vehicle.query.count() == 2  # Only the two from fixture should remain


def test_get_all(init_database, setup_salon_and_vehicles):
    _, vehicle1, vehicle2 = setup_salon_and_vehicles

    # Progress
    vehicles = VehicleRepository.get_all()

    # Assertions
    assert len(vehicles) == 2
    assert vehicle1 in vehicles
    assert vehicle2 in vehicles


def test_get_by_id(init_database, setup_salon_and_vehicles):
    _, vehicle1, _ = setup_salon_and_vehicles

    # Progress
    fetched_vehicle = VehicleRepository.get_by_id(vehicle1.id)

    # Assertions
    assert fetched_vehicle.id == vehicle1.id
    assert fetched_vehicle.name == 'Test Car 1'


def test_update(init_database, setup_salon_and_vehicles):
    _, vehicle1, _ = setup_salon_and_vehicles

    # Progress
    updated_vehicle = VehicleRepository.update(vehicle1.id, {'name': 'Updated Car'})

    # Assertions
    assert updated_vehicle.name == 'Updated Car'
    assert Vehicle.query.get(vehicle1.id).name == 'Updated Car'


def test_delete(init_database, setup_salon_and_vehicles):
    _, vehicle1, _ = setup_salon_and_vehicles

    # Progress
    VehicleRepository.delete(vehicle1)

    # Assertions
    assert Vehicle.query.get(vehicle1.id) is None
    assert Vehicle.query.count() == 1  # Only one vehicle should remain
