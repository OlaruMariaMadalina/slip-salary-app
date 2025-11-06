from app.auth.jwt_utils import create_access_token
from app.auth.password_utils import (
    hash_password,
    verify_password,
)
from app.db.repositories.user_repository import (
    get_user_by_username,
    create_user
)
from app.db.repositories.employee_repository import get_employee_by_email, is_department_manager
from app.db.db_deps import get_session

from fastapi import Depends, status, APIRouter, HTTPException
from app.schemas.user import TokenResponse, User
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(
    data: User | None,
    session: AsyncSession = Depends(get_session),
):
    employee = await get_employee_by_email(session, data.email)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if not await is_department_manager(session, employee.id):
        raise HTTPException(status_code=403, detail="Only department managers can register")
    
    existing_user = await get_user_by_username(session, employee.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists for this employee")
    
    hashed_password = hash_password(data.password)
    try:
        user = await create_user(session, employee.id, employee.email, hashed_password, "manager")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"msg": f"User '{user.username}' registered successfully"}


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login_user(
    data: User | None,
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_username(session, data.email)
    if not user or not verify_password(data.password, getattr(user, "hashed_password", "")):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    token = create_access_token(user_id=user.id)
    return TokenResponse(access_token=token, token_type="bearer")