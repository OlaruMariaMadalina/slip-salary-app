from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_account import UserAccount
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

async def get_user_by_username(db: AsyncSession, username: str) -> UserAccount | None:
    res = await db.execute(select(UserAccount).where(UserAccount.username == username))
    return res.scalars().first()

async def get_user_by_employee_id(db: AsyncSession, employee_id: int) -> UserAccount | None:
    res = await db.execute(select(UserAccount).where(UserAccount.employee_id == employee_id))
    return res.scalars().first()

async def get_user_by_user_id(db: AsyncSession, user_id: int) -> UserAccount | None:
    res = await db.execute(select(UserAccount).where(UserAccount.id == user_id))
    return res.scalars().first()

async def create_user(
    db: AsyncSession,
    employee_id: int,
    username_email: str,
    hashed_password: str,
    role: str = "user",
) -> UserAccount:
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