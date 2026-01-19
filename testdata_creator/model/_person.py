from typing import TYPE_CHECKING, override

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from ._deal import Deal


class PersonGroupAssociation(Base):
    __tablename__: str = "person_group_association_table"
    person_id: Mapped[int] = mapped_column(
        ForeignKey(column="person.id"), primary_key=True, nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey(column="group_table.id"), primary_key=True, nullable=False
    )
    person: Mapped["Person"] = relationship(back_populates="group_associations")
    group: Mapped["Group"] = relationship(back_populates="person_associations")


class Person(Base):
    __tablename__: str = "person"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(length=30))
    first_name: Mapped[str | None] = mapped_column(String(length=30))

    deals: Mapped[list[Deal]] = relationship("Deal", back_populates="person")

    group_associations: Mapped[list["PersonGroupAssociation"]] = relationship(
        back_populates="person"
    )

    groups: Mapped[list["Group"]] = relationship(
        secondary="person_group_association_table",
        back_populates="persons",
        viewonly=True,
    )

    @override
    def __repr__(self) -> str:
        return f"Person(id={self.id!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, groups={len(self.group_associations)}, deals={len(self.deals)})"


class Group(Base):
    __tablename__: str = "group_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30))

    person_associations: Mapped[list["PersonGroupAssociation"]] = relationship(
        back_populates="group"
    )

    persons: Mapped[list["Person"]] = relationship(
        secondary="person_group_association_table",
        back_populates="groups",
        viewonly=True,
    )

    @override
    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, name={self.name!r}, members={len(self.person_associations)})"
