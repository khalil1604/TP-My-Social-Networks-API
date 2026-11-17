from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def _email_taken(db: Session, email: str, exclude_id: int | None = None) -> bool:
    query = select(User).where(User.email == email)
    if exclude_id is not None:
        query = query.where(User.id != exclude_id)
    return db.scalar(query) is not None


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if _email_taken(db, data.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email déjà utilisé")
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=list[UserOut])
def search_users(
    q: str | None = Query(None, description="Recherche sur nom, prénom ou email"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = select(User)
    if q:
        pattern = f"%{q}%"
        query = query.where(
            or_(
                User.nom.ilike(pattern),
                User.prenom.ilike(pattern),
                User.email.ilike(pattern),
            )
        )
    return db.scalars(query.order_by(User.id).offset(skip).limit(limit)).all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")
    changes = data.model_dump(exclude_unset=True)
    if "email" in changes and _email_taken(db, changes["email"], exclude_id=user_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email déjà utilisé")
    for field, value in changes.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Utilisateur introuvable")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)