from typing import override

from sqlalchemy import ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base


class Deal(Base):
    __tablename__: str = "deal"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"), nullable=False)

    description: Mapped[str] = mapped_column(String(30))
    price_cent: Mapped[SmallInteger] = mapped_column()
    price_euro: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()

    @override
    def __repr__(self) -> str:
        return f"Deal(id={self.id!r}, description={self.description!r}, quantity={self.quantity!r}, price={self.price_euro!r}.{self.price_cent!r})"
