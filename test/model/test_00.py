from testdata_creator.model import Group, Person, PersonGroupAssociation


def test_00_basicmodel():
    person: Person = Person()
    person.id = 1
    person.first_name = "John"
    person.last_name = "Smith"
    assert "Person(id=1, first_name='John', last_name='Smith')" == f"{person!r}"


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
    assert "Person(id=1, first_name='Jane', last_name='Doe')" == f"{person_1!r}"
