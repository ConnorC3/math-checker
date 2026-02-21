from fastapi import FastAPI
from app.api.check import router as check_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Math Step Checker MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(check_router)
