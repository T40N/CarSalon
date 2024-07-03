import pytest
from app.models import User
from app.repositories import UserRepository
from app import db


@pytest.fixture(scope='function')
def setup_users(init_database):
    user1, user2 = None, None
    try:
        user1 = User(name='Test User 1')
        user2 = User(name='Test User 2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        yield user1, user2
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        if user1:
            db.session.delete(user1)
        if user2:
            db.session.delete(user2)
        db.session.commit()


def test_create(init_database):
    # Initialisation
    user = User(name='New User')

    # Progress
    created_user = UserRepository.create(user)

    # Assertions
    assert created_user.name == 'New User'
    assert User.query.count() == 1

    # Cleanup
    db.session.delete(created_user)
    db.session.commit()
    assert User.query.count() == 0


def test_get_all(init_database, setup_users):
    # Initialisation
    user1, user2 = setup_users

    # Progress
    users = UserRepository.get_all()

    # Assertions
    assert len(users) == 2
    assert user1 in users
    assert user2 in users


def test_get_by_id(init_database, setup_users):
    # Initialisation
    user1, _ = setup_users

    # Progress
    fetched_user = UserRepository.get_by_id(user1.id)

    # Assertions
    assert fetched_user.id == user1.id
    assert fetched_user.name == 'Test User 1'


def test_update(init_database, setup_users):
    # Initialisation
    user1, _ = setup_users

    # Progress
    updated_user = UserRepository.update(user1.id, {'name': 'Updated User'})

    # Assertions
    assert updated_user.name == 'Updated User'
    assert User.query.get(user1.id).name == 'Updated User'


def test_delete(init_database, setup_users):
    # Initialisation
    user1, _ = setup_users

    # Progress
    UserRepository.delete(user1)

    # Assertions
    assert User.query.get(user1.id) is None
    assert User.query.count() == 1
