from fastapi import FastAPI
from app.api.check import router as check_router

app = FastAPI(title="Math Step Checker MVP")
app.include_router(check_router)
