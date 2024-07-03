import pytest
from app.controllers import UserController
from app.models import User
from app.models import Vehicle
from app.models import Salon
from app import db


@pytest.fixture(scope='function')
def setup_salon_and_user(init_database):
    salon = Salon(name='Test Salon')
    user = User(name='Test User')
    db.session.add(salon)
    db.session.add(user)
    db.session.commit()

    yield salon, user

    db.session.delete(salon)
    db.session.delete(user)
    db.session.commit()


def test_create_user(init_database):
    # Initialisation
    data = {'name': 'Test User'}

    # Progress
    user = UserController.create_user(data)

    # Assertions
    assert user.name == 'Test User'
    assert User.query.count() == 1

    # Cleanup
    db.session.delete(user)
    db.session.commit()
    assert User.query.count() == 0


def test_get_all_users(init_database):
    # Initialisation
    user1 = User(name='User 1')
    user2 = User(name='User 2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Progress
    users = UserController.get_all_users()

    # Assertions
    assert len(users) == 2
    assert user1 in users
    assert user2 in users

    # Cleanup
    db.session.delete(user1)
    db.session.delete(user2)
    db.session.commit()
    assert User.query.count() == 0


def test_get_user_by_id(init_database):
    # Initialisation
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()
    user_id = user.id

    # Progress
    fetched_user = UserController.get_user_by_id(user_id)

    # Assertions
    assert fetched_user.id == user_id
    assert fetched_user.name == 'Test User'

    # Cleanup
    db.session.delete(user)
    db.session.commit()
    assert User.query.count() == 0


def test_update_user(init_database):
    # Initialisation
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()
    user_id = user.id

    update_data = {'name': 'Updated User'}

    # Progress
    updated_user = UserController.update_user(user_id, update_data)

    # Assertions
    assert updated_user.name == 'Updated User'
    assert User.query.get(user_id).name == 'Updated User'

    # Cleanup
    db.session.delete(updated_user)
    db.session.commit()
    assert User.query.count() == 0


def test_delete_user(init_database):
    # Initialisation
    user = User(name='Test User')
    db.session.add(user)
    db.session.commit()
    user_id = user.id

    # Progress
    success = UserController.delete_user(user_id)

    # Assertions
    assert success
    assert User.query.get(user_id) is None

    # Cleanup
    assert User.query.count() == 0


def test_assign_vehicle_to_user(init_database, setup_salon_and_user):
    salon, user = setup_salon_and_user
    # Initialisation
    car = Vehicle(name='Test Car', salon_id=salon.id)
    db.session.add(car)
    db.session.commit()

    # Progress
    user_with_vehicle = UserController.assign_vehicle_to_user(user.id, car.id)

    # Assertions
    assert user_with_vehicle.id == user.id
    assert car in user_with_vehicle.vehicles
    assert car.user_id == user.id

    # Cleanup
    db.session.delete(car)
    db.session.commit()
    assert Vehicle.query.count() == 0
