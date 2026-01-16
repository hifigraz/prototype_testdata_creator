from sqlalchemy import select
from sqlalchemy.orm import Session

import testdata_creator.config
import testdata_creator.engine
import testdata_creator.model


def _create_engine():
    return testdata_creator.engine.create_engine(
        testdata_creator.config.get_test_config().connection_string
    )


def _create_person(session: Session, first_name: str, last_name: str):
    person = testdata_creator.model.Person()
    person.first_name = first_name
    person.last_name = last_name
    session.add(person)
    session.commit
    return person


def _create_group(
    session: Session, name: str, persons: list[testdata_creator.model.Person]
):
    group = testdata_creator.model.Group()
    group.name = name
    for person in persons:
        a = testdata_creator.model.PersonGroupAssociation()
        a.person = person
        group.person_associations.append(a)
        session.add(a)
    session.add(group)
    session.commit()
    return group


def test_00_create_person():
    engine = _create_engine()
    with Session(engine) as session:
        _ = _create_person(session, "John", "Smith")

        stmt = select(testdata_creator.model.Person)
        for person in session.scalars(stmt):
            assert person.first_name == "John"
            assert person.last_name == "Smith"
            assert person.id > 0


def test_01_create_persons_and_groups():
    engine = _create_engine()
    with Session(bind=engine) as session:
        john = _create_person(session, first_name="John", last_name="Smith")
        jane = _create_person(session, first_name="Jane", last_name="Smith")

        users = _create_group(session, "USERS", [john, jane])
        admins = _create_group(session, "ADMINS", [jane])

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
