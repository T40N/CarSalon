import pytest
from datetime import date
from app.controllers import VehicleController
from app.models import Vehicle
from app.models import Salon
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


def test_create_vehicle(init_database, setup_salon):
    salon = setup_salon
    # Initialisation
    data = {
        'name': 'Test Car',
        'salon_id': salon.id
    }

    # Progress
    vehicle = VehicleController.create_vehicle(data)

    # Assertions
    assert vehicle.name == 'Test Car'
    assert vehicle.salon_id == salon.id
    assert Vehicle.query.count() == 1

    # Cleanup
    db.session.delete(vehicle)
    db.session.commit()
    assert Vehicle.query.count() == 0


def test_get_all_vehicles(init_database, setup_salon):
    salon = setup_salon
    # Initialisation
    car = Vehicle(name='Car 1', salon_id=salon.id)
    bicycle = Vehicle(name='Bicycle 1', salon_id=salon.id)
    db.session.add(car)
    db.session.add(bicycle)
    db.session.commit()

    # Progress
    vehicles = VehicleController.get_all_vehicles()

    # Assertions
    assert len(vehicles) == 2
    assert car in vehicles
    assert bicycle in vehicles

    # Cleanup
    db.session.delete(car)
    db.session.delete(bicycle)
    db.session.commit()
    assert Vehicle.query.count() == 0
    assert Vehicle.query.count() == 0


def test_get_vehicle_by_id(init_database, setup_salon):
    salon = setup_salon
    # Initialisation
    car = Vehicle(name='Car 1', salon_id=salon.id)
    db.session.add(car)
    db.session.commit()
    vehicle_id = car.id

    # Progress
    fetched_vehicle = VehicleController.get_vehicle_by_id(vehicle_id)

    # Assertions
    assert fetched_vehicle.id == vehicle_id
    assert fetched_vehicle.name == 'Car 1'

    # Cleanup
    db.session.delete(car)
    db.session.commit()
    assert Vehicle.query.count() == 0


def test_update_vehicle(init_database, setup_salon):
    salon = setup_salon
    # Initialisation
    car = Vehicle(name='Car 1', salon_id=salon.id)
    db.session.add(car)
    db.session.commit()
    vehicle_id = car.id

    update_data = {'name': 'Updated Car'}

    # Progress
    updated_vehicle = VehicleController.update_vehicle(vehicle_id, update_data)

    # Assertions
    assert updated_vehicle.name == 'Updated Car'
    assert Vehicle.query.get(vehicle_id).name == 'Updated Car'

    # Cleanup
    db.session.delete(updated_vehicle)
    db.session.commit()
    assert Vehicle.query.count() == 0


def test_delete_vehicle(init_database, setup_salon):
    salon = setup_salon
    # Initialisation
    car = Vehicle(name='Car 1', salon_id=salon.id)
    db.session.add(car)
    db.session.commit()
    vehicle_id = car.id

    # Progress
    success = VehicleController.delete_vehicle(vehicle_id)

    # Assertions
    assert success
    assert Vehicle.query.get(vehicle_id) is None

    # Cleanup
    assert Vehicle.query.count() == 0


def test_pay_monthly_fee(init_database, setup_salon):
    salon = setup_salon
    # Initialisation
    car = Vehicle(name='Car 1', salon_id=salon.id)
    db.session.add(car)
    db.session.commit()
    vehicle_id = car.id

    payment_data = {'amount': 100}

    # Progress
    updated_vehicle = VehicleController.pay_monthly_fee(vehicle_id, payment_data['amount'])

    # Assertions
    assert updated_vehicle.total_cost == 100

    # Cleanup
    db.session.delete(updated_vehicle)
    db.session.commit()
    assert Vehicle.query.count() == 0
