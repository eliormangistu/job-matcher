from app.core.exceptions import UserAlreadyExistsException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User, UserAuth
from app.core.logger import ServiceLogger
from app.core.security.password import hash_password
from app.repositories.user_auth import create as create_user_auth


logger = ServiceLogger("user_repository")


def get_by_google_id(
    db: Session,
    google_id: str,
) -> User | None:
    logger.info(
        "Fetching user by Google ID",
        action="get_by_google_id",
    )

    user = db.scalar(select(User).where(User.google_id == google_id))

    logger.info(
        "User lookup completed",
        action="get_by_google_id",
        found=user is not None,
    )

    return user


def get_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    logger.info(
        "Fetching user by id",
        action="get_by_id",
        user_id=user_id,
    )

    user = db.get(User, user_id)

    logger.info(
        "User lookup completed",
        action="get_by_id",
        user_id=user_id,
        found=user is not None,
    )

    return user


def create(
    db: Session,
    user: User,
) -> User:
    logger.info(
        "Creating user",
        action="create",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(
        "User created",
        action="create",
        user_id=user.id,
    )

    return user


def add(
    db: Session,
    user: User,
) -> User:
    logger.info(
        "Adding user",
        action="add",
    )

    db.add(user)
    db.flush()

    logger.info(
        "User added",
        action="add",
        user_id=user.id,
    )

    return user


def get_by_email(
    db: Session,
    email: str,
) -> User | None:
    logger.info(
        "Fetching user by email",
        action="get_by_email",
    )

    user = db.scalar(select(User).where(User.email == email))

    logger.info(
        "User lookup completed",
        action="get_by_email",
        found=user is not None,
    )

    return user


def register_user(
    db: Session,
    email: str,
    name: str,
    password: str,
) -> User:
    logger.info(
        "Registering new user",
        action="register_user",
    )

    existing_user = get_by_email(
        db=db,
        email=email,
    )

    if existing_user is not None:
        logger.warning(
            "User registration rejected",
            action="register_user",
            reason="email_already_exists",
        )
        raise UserAlreadyExistsException("Email already registered")

    user = User(
        email=email,
        name=name,
        google_id=None,
    )

    user = create(
        db=db,
        user=user,
    )

    password_hash = hash_password(password)

    user_auth = UserAuth(
        user_id=user.id,
        password_hash=password_hash,
    )

    create_user_auth(
        db=db,
        user_auth=user_auth,
    )

    logger.info(
        "User registered successfully",
        action="register_user",
        user_id=user.id,
    )

    return user


def delete(
    db: Session,
    user: User,
) -> None:
    logger.info(
        "Deleting user",
        action="delete_user",
        user_id=user.id,
    )

    try:
        db.delete(user)
        db.commit()

        logger.info(
            "User deleted",
            action="delete_user",
            user_id=user.id,
        )

    except Exception:
        db.rollback()

        logger.exception(
            "Failed to delete user",
            action="delete_user",
            user_id=user.id,
        )

        raise
