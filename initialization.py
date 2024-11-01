from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import get_db, engine
from enums import UserRole
from models import User, entities

from config import get_settings

settings = get_settings()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin_user(db: Session):
    admin = db.query(User).filter(User.role == UserRole.ADMIN.value).first()
    if admin:
        print("Admin already exists")
        return

    admin_user = User(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=password_context.hash(settings.ADMIN_PASSWORD),
        role=UserRole.ADMIN.value,
    )

    try:
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user created")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error while creating admin user: {e}")


def initialize_db():
    entities.Base.metadata.create_all(bind=engine)

    db = next(get_db())
    create_admin_user(db)
    db.close()
