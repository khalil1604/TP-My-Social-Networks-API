from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event, EventUser, User
from app.schemas import EventCreate, EventOut, EventUpdate

router = APIRouter(prefix="/events", tags=["Events"])


def _get_event(db: Session, event_id: int) -> Event:
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Événement introuvable")
    return event


@router.post("", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    ids = set(data.organisateur_ids)
    found = db.scalars(select(User.id).where(User.id.in_(ids))).all()
    if len(found) != len(ids):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Organisateur introuvable")

    event = Event(**data.model_dump(exclude={"organisateur_ids"}))
    event.members = [EventUser(user_id=i, role="organizer") for i in ids]
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("", response_model=list[EventOut])
def search_events(
    q: str | None = Query(None, description="Recherche sur nom ou lieu"),
    visibilite: str | None = Query(None, pattern="^(public|private)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = select(Event)
    if q:
        pattern = f"%{q}%"
        query = query.where(or_(Event.nom.ilike(pattern), Event.lieu.ilike(pattern)))
    if visibilite:
        query = query.where(Event.visibilite == visibilite)
    return db.scalars(query.order_by(Event.id).offset(skip).limit(limit)).all()


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return _get_event(db, event_id)


@router.patch("/{event_id}", response_model=EventOut)
def update_event(event_id: int, data: EventUpdate, db: Session = Depends(get_db)):
    event = _get_event(db, event_id)
    changes = data.model_dump(exclude_unset=True)
    debut = changes.get("date_debut", event.date_debut)
    fin = changes.get("date_fin", event.date_fin)
    if fin <= debut:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "date_fin doit être après date_debut"
        )
    for field, value in changes.items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = _get_event(db, event_id)
    db.delete(event)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{event_id}/participants/{user_id}",
    response_model=EventOut,
    status_code=status.HTTP_201_CREATED,
)
def add_participant(event_id: int, user_id: int, db: Session = Depends(get_db)):
    event = _get_event(db, event_id)
    if not db.get(User, user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")
    if db.get(EventUser, (event_id, user_id)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Déjà membre de cet événement")
    db.add(EventUser(event_id=event_id, user_id=user_id, role="participant"))
    db.commit()
    db.refresh(event)
    return event


@router.delete(
    "/{event_id}/participants/{user_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_participant(event_id: int, user_id: int, db: Session = Depends(get_db)):
    member = db.get(EventUser, (event_id, user_id))
    if not member or member.role != "participant":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Participant introuvable")
    db.delete(member)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)