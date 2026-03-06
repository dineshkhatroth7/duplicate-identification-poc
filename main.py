from fastapi import FastAPI
from api.routers import router as api_router

app = FastAPI(title= "SmartRecruitz AI Agents")

app.include_router(api_router)