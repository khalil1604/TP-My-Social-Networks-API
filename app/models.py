from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nom: Mapped[str] = mapped_column(String(255))
    prenom: Mapped[str] = mapped_column(String(255))
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )




class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_debut: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    date_fin: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    lieu: Mapped[str] = mapped_column(String(255))
    photo_couverture: Mapped[str | None] = mapped_column(String(500), nullable=True)
    visibilite: Mapped[str] = mapped_column(String(10), default="public")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    members: Mapped[list["EventUser"]] = relationship(
        cascade="all, delete-orphan"
    )


class EventUser(Base):
    """Table d'association plusieurs-à-plusieurs : utilisateur <-> événement."""

    __tablename__ = "event_users"

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str] = mapped_column(String(20)) 