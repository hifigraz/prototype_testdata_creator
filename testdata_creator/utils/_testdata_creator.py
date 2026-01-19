# testdata creator main module
import getopt
import os
import sys
import random

import faker

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from testdata_creator.model import Deal, Group, Person, PersonGroupAssociation
from  testdata_creator.engine import create_engine

from ..config import get_logger

logger = get_logger()

USAGE_FORMAT_STR = "%s [-h|--help] (-c <connection_string> | --connection-string=<connection-string>) [-v|--verbose] [-n <number_of_persons> | --number=<number_of_persons>%s%s"
USAGE_STRING = """
     -h --help                      : display this help message and exit.
     -v --verbose                   : increase verbosity.
     -c --connection-string=<value> : connection string for database to use.
     -n --number=<value>            : number of persons to create
"""

engine : Engine| None = None

def _print_ussage():
    program_name = os.path.basename(sys.argv[0])
    print(USAGE_FORMAT_STR % (program_name, os.linesep, USAGE_STRING))


def _create_engine(connection_string:str=""):
    global engine
    if not engine:
       engine =  create_engine(connection_string)
    return engine


def _create_groups():
    group_names = [
        "USER",
        "ADMIN",
        "RED",
        "GREEN",
        "BLUE",
        "BLACK",
    ]
    engine = _create_engine()
    with Session(engine) as session:
        for group_name in group_names:
            group = Group(name=group_name)
            session.add(group)
        session.commit()
    return group_names


def _add_group(session:Session, person:Person, group:Group):
    person_group_association = PersonGroupAssociation()
    person_group_association.person = person
    group.person_associations.append(person_group_association)
    session.add_all([person, group, person_group_association])


def _create_deals(session: Session, person:Person):
    for i in range(random.randint(500,1500)):
        deal = Deal()
        deal.description = f"Testdeal for {person.first_name} {person.last_name} {i}"
        deal.price_cent = random.randint(0,99)
        deal.price_euro = random.randint(10,1000)
        deal.quantity = random.randint(1,10)*random.choice([-1,1])
        person.deals.append(deal)
        session.add_all([person, deal])


def _create_persons(number:int) -> list[int]:
    person_ids: list[int] = []
    group_names=  _create_groups()
    _faker = faker.Faker()
    _engine = _create_engine()
    with Session(engine) as session:
        groups:list[Group] = []
        for group_name in group_names: # do this to get users group at first place.... FIXXXME
            group_stmt = select(Group).where(Group.name==group_name)
            group = session.execute(group_stmt).scalars().first()
            assert group
            groups.append(group)
        while number:
            person = Person()
            person.first_name = _faker.first_name()
            person.last_name = _faker.last_name()
            _add_group(session, person, groups[0])
            for additional_group in random.sample(groups[1:],random.randint(0,2)):
                _add_group(session, person, additional_group)
            _create_deals(session,person)
            person_ids.append(person.id)
            session.commit() # This is bad for performance, but good for debugging.
            logger.debug(person)
            number-=1
    return person_ids
    

def testdata_creator():
    opts = []
    args = []
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvc:vn:v",
            ["help", "verbose", "connection-string=", "number="],
        )
    except getopt.GetoptError as err:
        logger.error("Error: %s", err)
        _print_ussage()
        sys.exit(1)

    number = 1000
    connection_string = ""
    help=False

    for o, a in opts:
        if o == "-v" or o == "--verbose":
            logger.setLevel("DEBUG")
        if o in ("-h", "--help"):
            help = True
        if o in ("-n", "--number"):
            number = int(a)
        if o in ("-c", "--connection_string"):
            connection_string = a
    
    logger.debug(opts)
    logger.debug(args)

    if help:
            _print_ussage()
            sys.exit(0)

    logger.debug("Connection String: >>%s<<", connection_string)
    logger.debug("Number of persons: >>%s<<", number)

    _ = _create_engine(connection_string)
    _ = _create_groups()
    person_ids = _create_persons(number)

    logger.debug(person_ids)


#  select d.description, p.first_name, p.last_name, g.name from deal d join person p on d.person_id=p.id join person_group_association_table pga on pga.person_id=p.id join 'group' g on pga.group_id=g.id where g.name like 'BLACK';
#  select d.description, p.first_name, p.last_name, g.name from 'group' g join person_group_association_table pga on pga.group_id=g.id join person p on p.id=pga.person_id join deal d on d.person_id=p.id where g.name like 'BLACK';

# time echo "select d.description, p.first_name, p.last_name, g.name from deal d join person p on d.person_id=p.id join person_group_association_table pga on pga.person_id=p.id join 'group' g on pga.group_id=g.id where g.name like 'BLACK';" | sqlite3 test.db 
# time echo "select d.description, p.first_name, p.last_name, g.name from 'group' g join person_group_association_table pga on pga.group_id=g.id join person p on p.id=pga.person_id join deal d on d.person_id=p.id where g.name like 'BLACK';" | sqlite3 test.db
