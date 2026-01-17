from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

import testdata_creator.model

from ._helper import create_engine, create_person, create_group, create_deal


def test_00_create_person():
    engine = create_engine()
    with Session(engine) as session:
        _ = create_person(session, "John", "Smith")

        stmt = select(testdata_creator.model.Person)
        for person in session.scalars(stmt):
            assert person.first_name == "John"
            assert person.last_name == "Smith"
            assert person.id > 0


def test_01_create_persons_and_groups():
    engine = create_engine()
    with Session(bind=engine) as session:
        john = create_person(session, first_name="John", last_name="Smith")
        jane = create_person(session, first_name="Jane", last_name="Smith")

        users = create_group(session, "USERS", [john, jane])
        admins = create_group(session, "ADMINS", [jane])

        assert len(users.person_associations) == 2
        assert len(admins.person_associations) == 1

        jane_found = False
        john_found = False
        for p in users.persons:
            assert p.last_name == "Smith"
            if p.first_name == "John":
                john_found = True
            if p.first_name == "Jane":
                jane_found = True

        assert jane_found == True
        assert john_found == True

        assert 2 == len(jane.groups)
        assert 1 == len(john.groups)

        stmt = select(testdata_creator.model.Group)
        for group in session.scalars(stmt):
            if group.name == "USERS":
                assert len(group.persons) == 2
            else:
                assert len(group.persons) == 1


def test_02_create_person_and_deals():
    engine = create_engine()
    with Session(bind=engine) as session:
        john = create_person(session, first_name="John", last_name="Smith")
        deal1 = create_deal(
            session,
            "test_deal",
            john,
            datetime(year=2026, month=1, day=17, hour=17, minute=0, second=0),
            4,
            10,
            50,
        )

        assert 0 == len(john.groups)
        assert 1 == len(john.deals)

        assert (
            "Person(id=1, first_name='John', last_name='Smith', groups=0, deals=1)"
            == f"{john}"
        )
        assert (
            "Deal(id=1, person='1:John Smith', date_time='2026-01-17 17:00:00', description='test_deal', quantity=4, price=10.50)"
            == f"{deal1}"
        )
