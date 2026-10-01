from app.core.security.password import hash_password, verify_password
from sqlalchemy.orm import Session

from app.models import User, UserAuth
from app.core.logger import ServiceLogger
from app.repositories.user import (
    add as add_user,
    get_by_email,
    delete,
    get_by_google_id,
    get_by_id,
    create,
)

from app.repositories.user_auth import (
    add as add_user_auth,
)
from app.core.exceptions import AuthenticationException, UserAlreadyExistsException
from app.repositories.user_auth import get_by_user_id

logger = ServiceLogger("user_service")


def get_or_create_user(
    db: Session,
    google_id: str,
    email: str,
    name: str,
) -> User:
    logger.info(
        "Getting or creating user",
        action="get_or_create_user",
        google_id=google_id,
    )

    user = get_by_google_id(
        db=db,
        google_id=google_id,
    )

    if user:
        logger.info(
            "Existing user found",
            action="get_or_create_user",
            user_id=user.id,
        )
        return user

    user = User(
        google_id=google_id,
        email=email,
        name=name,
    )

    user = create(
        db=db,
        user=user,
    )

    logger.info(
        "New user created",
        action="get_or_create_user",
        user_id=user.id,
    )

    return user


def get_current_user(
    db: Session,
    user_id: int,
) -> User | None:
    logger.info(
        "Fetching current user",
        action="get_current_user",
        user_id=user_id,
    )

    user = get_by_id(
        db=db,
        user_id=user_id,
    )

    logger.info(
        "Current user fetched",
        action="get_current_user",
        user_id=user_id,
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

    try:
        user = User(
            email=email,
            name=name,
            google_id=None,
        )

        user = add_user(
            db=db,
            user=user,
        )

        password_hash = hash_password(password)

        user_auth = UserAuth(
            user_id=user.id,
            password_hash=password_hash,
        )

        add_user_auth(
            db=db,
            user_auth=user_auth,
        )

        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise

    logger.info(
        "User registered successfully",
        action="register_user",
        user_id=user.id,
    )

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    logger.info(
        "User login started",
        action="login_user",
    )

    user = get_by_email(
        db=db,
        email=email,
    )

    if user is None:
        logger.warning(
            "User login failed",
            action="login_user",
            reason="invalid_credentials",
        )
        raise AuthenticationException("Invalid email or password")

    user_auth = get_by_user_id(
        db=db,
        user_id=user.id,
    )

    if user_auth is None:
        logger.warning(
            "User login failed",
            action="login_user",
            reason="auth_credentials_not_found",
            user_id=user.id,
        )
        raise AuthenticationException("Invalid email or password")

    if not verify_password(
        password,
        user_auth.password_hash,
    ):
        logger.warning(
            "User login failed",
            action="login_user",
            reason="invalid_credentials",
            user_id=user.id,
        )
        raise AuthenticationException("Invalid email or password")

    logger.info(
        "User login successful",
        action="login_user",
        user_id=user.id,
    )

    return user


def delete_user(
    db: Session,
    user: User,
) -> None:
    logger.info(
        "Deleting user account",
        action="delete_user",
        user_id=user.id,
    )

    delete(
        db=db,
        user=user,
    )

    logger.info(
        "User account deleted",
        action="delete_user",
        user_id=user.id,
    )
