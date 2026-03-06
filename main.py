from fastapi import FastAPI
from api.routes import app as api_router

app = FastAPI(title= "Smart Recruitz AI")

app.include_router(api_router)