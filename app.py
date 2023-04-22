from fastapi import FastAPI
from route.router import router
from models import models
from config.database import SessionLocal, engine
models.Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(router)