from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, password: str, full_name: str):
    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        role="USER",
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_users(db: Session, search: str | None = None, is_active: bool | None = None):
    query = db.query(User)

    if search:
        search_value = f"%{search}%"

        query = query.filter(
            (User.full_name.ilike(search_value)) | (User.email.ilike(search_value))
        )

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.order_by(User.id.asc()).all()
