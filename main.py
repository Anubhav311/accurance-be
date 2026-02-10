import openpyxl
from pathlib import Path
from docxtpl import DocxTemplate
from fastapi import FastAPI
from app.routers.meetings import router as meetings_router
from app.routers.company import router as company_router
from app.routers.health import router as health_router
from fastapi.middleware.cors import CORSMiddleware

from conf import settings



app = FastAPI(title="Meeting Document Generator")

origins = settings.origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(meetings_router)
app.include_router(company_router)
app.include_router(health_router)