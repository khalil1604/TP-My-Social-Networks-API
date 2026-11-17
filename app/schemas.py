from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from typing import Literal

from pydantic import model_validator

class UserCreate(BaseModel):
    email: EmailStr
    nom: str = Field(min_length=1, max_length=255)
    prenom: str = Field(min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=0, le=150)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    nom: str | None = Field(default=None, min_length=1, max_length=255)
    prenom: str | None = Field(default=None, min_length=1, max_length=255)
    age: int | None = Field(default=None, ge=0, le=150)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    nom: str
    prenom: str
    age: int | None
    created_at: datetime




class EventCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=255)
    description: str | None = None
    date_debut: datetime
    date_fin: datetime
    lieu: str = Field(min_length=1, max_length=255)
    photo_couverture: str | None = None
    visibilite: Literal["public", "private"] = "public"
    organisateur_ids: list[int] = Field(min_length=1)

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_fin <= self.date_debut:
            raise ValueError("date_fin doit être après date_debut")
        return self


class EventUpdate(BaseModel):
    nom: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    date_debut: datetime | None = None
    date_fin: datetime | None = None
    lieu: str | None = Field(default=None, min_length=1, max_length=255)
    photo_couverture: str | None = None
    visibilite: Literal["public", "private"] | None = None


class MemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    role: str


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nom: str
    description: str | None
    date_debut: datetime
    date_fin: datetime
    lieu: str
    photo_couverture: str | None
    visibilite: str
    created_at: datetime
    members: list[MemberOut]