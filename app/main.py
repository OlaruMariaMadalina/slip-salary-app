from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.routers.management_router import router as management_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(management_router)