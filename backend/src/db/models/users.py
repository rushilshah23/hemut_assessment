from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class RoleORM(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )
    
    
class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)

    role_id: Mapped[str] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )

    role = relationship("RoleORM")

class AdminORM(Base):
    __tablename__ = "admins"

    id: Mapped[str] = mapped_column(primary_key=True)

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    user = relationship("UserORM")
    
    
class GuestORM(Base):
    __tablename__ = "guests"

    id: Mapped[str] = mapped_column(primary_key=True)

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    user = relationship("UserORM")