from datetime import datetime
from sqlalchemy.orm import Session

import testdata_creator.config
import testdata_creator.engine
import testdata_creator.model


def create_engine():
    return testdata_creator.engine.create_engine(
        testdata_creator.config.get_test_config().connection_string
    )


def create_person(session: Session, first_name: str, last_name: str):
    person = testdata_creator.model.Person()
    person.first_name = first_name
    person.last_name = last_name
    session.add(person)
    session.commit
    return person


def create_group(
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


def create_deal(
    session: Session,
    description: str,
    person: testdata_creator.model.Person,
    date_time: datetime,
    quantity: int,
    price_euro: int,
    price_cent: int,
):
    deal = testdata_creator.model.Deal()
    deal.person = person
    deal.date_time = date_time
    deal.description = description
    deal.quantity = quantity
    deal.price_euro = price_euro
    deal.price_cent = price_cent
    session.add(deal)
    session.commit()
    return deal
