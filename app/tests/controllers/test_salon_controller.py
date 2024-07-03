import pytest
from app.controllers.salon_controller import SalonController
from app.models.salon import Salon
from app import db


def test_create_salon(init_database):
    # Initialisation
    data = {'name': 'Salon Testowy'}

    # Progress
    salon = SalonController.create_salon(data)

    # Assertions
    assert salon.name == 'Salon Testowy'
    assert Salon.query.count() == 1

    # Cleanup
    db.session.delete(salon)
    db.session.commit()
    assert Salon.query.count() == 0


def test_get_all_salons(init_database):
    # Initialisation
    salon1 = Salon(name='Salon Testowy 1')
    salon2 = Salon(name='Salon Testowy 2')
    db.session.add(salon1)
    db.session.add(salon2)
    db.session.commit()

    # Progress
    salons = SalonController.get_all_salons()

    # Assertions
    assert len(salons) == 2
    assert salon1 in salons
    assert salon2 in salons

    # Cleanup
    db.session.delete(salon1)
    db.session.delete(salon2)
    db.session.commit()
    assert Salon.query.count() == 0


def test_get_salon_by_id(init_database):
    # Initialisation
    salon = Salon(name='Salon Testowy')
    db.session.add(salon)
    db.session.commit()
    salon_id = salon.id

    # Progress
    fetched_salon = SalonController.get_salon_by_id(salon_id)

    # Assertions
    assert fetched_salon.id == salon_id
    assert fetched_salon.name == 'Salon Testowy'

    # Cleanup
    db.session.delete(salon)
    db.session.commit()
    assert Salon.query.count() == 0


def test_update_salon(init_database):
    # Initialisation
    salon = Salon(name='Salon Testowy')
    db.session.add(salon)
    db.session.commit()
    salon_id = salon.id

    update_data = {'name': 'Salon Zaktualizowany'}

    # Progress
    updated_salon = SalonController.update_salon(salon_id, update_data)

    # Assertions
    assert updated_salon.name == 'Salon Zaktualizowany'
    assert Salon.query.get(salon_id).name == 'Salon Zaktualizowany'

    # Cleanup
    db.session.delete(updated_salon)
    db.session.commit()
    assert Salon.query.count() == 0


def test_delete_salon(init_database):
    # Initialisation
    salon = Salon(name='Salon Testowy')
    db.session.add(salon)
    db.session.commit()
    salon_id = salon.id

    # Progress
    success = SalonController.delete_salon(salon_id)

    # Assertions
    assert success
    assert Salon.query.get(salon_id) is None

    # Cleanup
    assert Salon.query.count() == 0
