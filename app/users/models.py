from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, int_pk, str_uniq


class User(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    email: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]

    is_user: Mapped[bool] = mapped_column(
        default=True,
        server_default=text('True'),
        nullable=False
    )
    is_vendor: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('False'),
        nullable=False
    )
    is_analyst: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('False'),
        nullable=False
    )
    is_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('false'),
        nullable=False
    )
    is_super_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('false'),
        nullable=False
    )

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
