from testdata_creator.model import Deal, Group, Person, PersonGroupAssociation


def test_00_basicmodel():
    person: Person = Person()
    person.id = 1
    person.first_name = "John"
    person.last_name = "Smith"
    assert (
        "Person(id=1, first_name='John', last_name='Smith', groups=0, deals=0)"
        == f"{person!r}"
    )


def test_01_basicmodel():

    person_1: Person = Person()
    person_1.id = 1
    person_1.first_name = "Jane"
    person_1.last_name = "Doe"

    person_2: Person = Person()
    person_2.id = 2
    person_2.first_name = "John"
    person_2.last_name = "Doe"

    group: Group = Group()
    group.id = 1
    group.name = "USER"

    association_1 = PersonGroupAssociation()
    association_1.group = group
    person_1.group_associations.append(association_1)

    association_2 = PersonGroupAssociation()
    association_2.group = group
    person_2.group_associations.append(association_2)

    assert "Group(id=1, name='USER', members=2)" == f"{group!r}"
    assert (
        "Person(id=1, first_name='Jane', last_name='Doe', groups=1, deals=0)"
        == f"{person_1!r}"
    )


def test_02_deals() -> None:

    person_1: Person = Person()
    person_1.id = 1
    person_1.first_name = "Jane"
    person_1.last_name = "Doe"

    deal_1 = Deal()
    deal_1.id = 1
    deal_1.price_cent = 50
    deal_1.price_euro = 10
    deal_1.quantity = 5
    deal_1.person = person_1
    deal_1.description = "description"

    assert (
        "Deal(id=1, person='1:Jane Doe', date_time='None', description='description', quantity=5, price=10.50)"
        == repr(deal_1)
    )
    assert (
        "Person(id=1, first_name='Jane', last_name='Doe', groups=0, deals=1)"
        == f"{deal_1.person}"
    )
