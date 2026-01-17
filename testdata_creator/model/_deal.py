# pyright: reportImportCycles = false
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, override

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base

if TYPE_CHECKING:
    from ._person import Person


class Deal(Base):
    __tablename__: str = "deal"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"), nullable=False)

    date_time: Mapped[datetime] = mapped_column(
        DateTime(True), server_default=func.now()
    )

    description: Mapped[str] = mapped_column(String(30))
    price_cent: Mapped[int] = mapped_column(
        CheckConstraint("price_cent BETWEEN 0 and 99")
    )
    price_euro: Mapped[int] = mapped_column(CheckConstraint("price_euro >= 0 "))
    quantity: Mapped[int] = mapped_column()

    person: Mapped["Person"] = relationship(back_populates="deals")

    @override
    def __repr__(self) -> str:
        return f"Deal(id={self.id!r}, person='{self.person.id}:{self.person.first_name} {self.person.last_name}', date_time='{self.date_time}', description={self.description!r}, quantity={self.quantity!r}, price={self.price_euro!r}.{self.price_cent!r:0>2})"
