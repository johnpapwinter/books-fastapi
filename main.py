from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from initialization import initialize_db
from routes import router as books_router
from routes import user_router
from routes import genre_router
from models import entities
from database import engine


@asynccontextmanager
async def lifespan(app_: FastAPI):
    initialize_db()
    yield

app = FastAPI(lifespan=lifespan)


# entities.Base.metadata.create_all(bind=engine)

app.include_router(books_router)
app.include_router(user_router)
app.include_router(genre_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
