from datetime import datetime
from sqlalchemy.orm import Session
from ._helper import create_deal, create_engine, create_person


def test_00_valid_prices():
    engine = create_engine()
    with Session(engine) as session:
        person = create_person(session, "John", "Smith")
        deal_1 = create_deal(session, "deal", person, datetime(year=2026, month=1,day=17, hour=17,minute=0,second=0), 0, 0, 0)
        person.deals.append(deal_1)
        session.add_all([person, deal_1])
        session.commit()
