from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_account import UserAccount
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

async def get_user_by_username(db: AsyncSession, username: str) -> UserAccount | None:
    """
    Retrieve a user account by username.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        username (str): The username or email of the user.

    Returns:
        UserAccount | None: The UserAccount object if found, otherwise None.
    """    
    res = await db.execute(select(UserAccount).where(UserAccount.username == username))
    return res.scalars().first()

async def get_user_by_employee_id(db: AsyncSession, employee_id: int) -> UserAccount | None:
    """
    Retrieve a user account by employee ID.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        employee_id (int): The ID of the employee.

    Returns:
        UserAccount | None: The UserAccount object if found, otherwise None.
    """
    res = await db.execute(select(UserAccount).where(UserAccount.employee_id == employee_id))
    return res.scalars().first()

async def get_user_by_user_id(db: AsyncSession, user_id: int) -> UserAccount | None:
    """
    Retrieve a user account by user ID.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        user_id (int): The ID of the user account.

    Returns:
        UserAccount | None: The UserAccount object if found, otherwise None.
    """
    res = await db.execute(select(UserAccount).where(UserAccount.id == user_id))
    return res.scalars().first()

async def create_user(
    db: AsyncSession,
    employee_id: int,
    username_email: str,
    hashed_password: str,
    role: str = "user",
) -> UserAccount:
    """
    Create and persist a new user account.

    Args:
        db (AsyncSession): The SQLAlchemy async session.
        employee_id (int): The ID of the employee associated with the user.
        username_email (str): The username or email for the user account.
        hashed_password (str): The hashed password for the user.
        role (str, optional): The role of the user. Defaults to "user".

    Returns:
        UserAccount: The created UserAccount object.

    Raises:
        ValueError: If a user already exists for this employee or the username is taken.
    """
    user = UserAccount(
        employee_id=employee_id,
        username=username_email,
        hashed_password=hashed_password,
        role=role,
        is_active=True,
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise ValueError("User already exists for this employee or username is taken.") from e
    await db.refresh(user)
    return user