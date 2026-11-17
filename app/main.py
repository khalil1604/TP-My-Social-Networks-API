from fastapi import FastAPI
from app.database import Base, engine
from app import models  # noqa: F401  (nécessaire pour que Base connaisse User)

from app.routers import users

from app.routers import events, users
...

Base.metadata.create_all(bind=engine)
app = FastAPI(title="My Social Networks API", version="1.0.0")

app.include_router(users.router)
app.include_router(events.router)


@app.get("/health")
def health():
    return {"status": "ok"}